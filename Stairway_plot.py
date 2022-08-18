import sys

keys = ['mutation_per_site', 'n_estimation', 'theta_per_site_median', 'theta_per_site_2_5', 'theta_per_site_97_5', 'year', 'Ne_median', 'Ne_2_5', 'Ne_97_5', 'Ne_12_5', 'Ne_87_5']
class Summary(object):
	def __init__(self, summary):
		self.summary = summary
	def __iter__(self):
		return self._parse()
	def _parse(self):
		i = 0
		for line in open(self.summary):
			i += 1
			if i == 1:
				continue
			line = line.strip().split('\t')
	#		print line
			yield SummaryRecord(*line)
class SummaryRecord(object):
	def __init__(self, *line):
#		print line
		for key, value in zip(keys, line):
			setattr(self, key, float(value))
#		print vars(self)

def plot_multi_summary(summary_files, outfig, lables=None, colors=None, alpha=0.2, fold=1, xmin=1000):
	import matplotlib.pyplot as plt
	data = []
	for summary_file in summary_files:
		data.append([rc for rc in Summary(summary_file)])
		
	if lables is None:
		lables = create_labels(summary_files)
	if colors is None:
		colors = create_colors(len(summary_files))
	
	plt.figure(figsize=(11, 5))
	xmins, ymins, xmaxs, ymaxs = [], [], [], []
#	xmin = 1
	for dat, label, color in zip(data, lables, colors):
	#	print >>sys.stderr, vars(dat[0])
		x = [rc.year * fold for rc in dat]
		y = [rc.Ne_median for rc in dat]
		y_2_5  = [rc.Ne_2_5  for rc in dat]
		y_97_5 = [rc.Ne_97_5 for rc in dat]
		y_12_5 = [rc.Ne_12_5 for rc in dat]
		y_87_5 = [rc.Ne_87_5 for rc in dat]
		if x[0] > xmin:
			x = [xmin] + x
			y = [y[0]] + y
			y_2_5 = [y_2_5[0]] + y_2_5
			y_97_5 = [y_97_5[0]] + y_97_5
			y_12_5 = [y_12_5[0]] + y_12_5
			y_87_5 = [y_87_5[0]] + y_87_5
		plt.plot(x, y, label=label, color=color, )
		plt.fill_between(x, y_2_5, y_97_5, color=color, alpha=alpha)
		plt.fill_between(x, y_12_5, y_87_5, color=color, alpha=alpha)
		mx = [v for v in x if v >=xmin]
		y_2_5 = [v for vx,v in zip(x,y_2_5) if vx >=xmin]
		y_97_5 = [v for vx,v in zip(x,y_97_5) if vx >=xmin]
		xmins += [min(mx)]
		ymins += [min(y_2_5)]
		xmaxs += [max(mx)]
		ymaxs += [max(y_97_5)]
#	print max(x)
#	xmin = 1 #max(xmins)
	ymin = min(ymins) * 0.5
	xmax = max(xmaxs) * 5
	ymax = max(ymaxs) * 10
	plt.legend(loc='best')
	plt.xlim(xmin, xmax)
	plt.ylim(ymin, ymax)
	plt.xscale('log')
	plt.yscale('log')
	plt.xlabel('Time (years ago)')
	plt.ylabel('Ne')
	plt.savefig(outfig)
def create_colors(n):
	import numpy as np
	from matplotlib import cm
#	from matplotlib.colors import ListedColormap
#	if n < 8:
#		colors = cm.get_cmap('Dark2')
	if n <=10:
		colors = cm.get_cmap('tab10')
	elif n <= 20:
		colors = cm.get_cmap('tab20')
	else:
		colors = cm.get_cmap('viridis', n)
	colors = colors(np.linspace(0, 1, n))
#	print >>sys.stderr, colors
	return colors
def create_label(summary_file):
	import os
	return os.path.basename(summary_file).split('.')[0]
def create_labels(summary_files):
	return [create_label(summary_file) for summary_file in summary_files]
def main():
	try: 
		fold = float(sys.argv[-1])
		outfig = sys.argv[-2]
		summary_files = sys.argv[1:-2]
	except ValueError:
		summary_files = sys.argv[1:-1]
		outfig = sys.argv[-1]
		fold = 1
	if outfig.startswith('summary'):
		raise ValueError('out figure {} seems to be error'.format(outfig))
	print >>sys.stderr, summary_files, outfig, fold
	plot_multi_summary(summary_files, outfig, fold=fold)
if __name__ == '__main__':
	main()
