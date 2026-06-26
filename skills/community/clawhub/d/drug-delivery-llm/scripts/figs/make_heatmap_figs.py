import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
plt.figure(dpi=300)
sns.heatmap(
    data=adj_,
    cmap=plt.get_cmap('tab20c'),  # Use matplotlib colormap 'tab20c'
    yticklabels=new_label3,
    # yticklabels=new_label,  # Alternative yticklabels if needed
)
plt.yticks(size=8)
plt.xticks(size=8)
plt.tick_params(top=False, bottom=True, left=False, right=False)
plt.title("Adjacency Matrix Heatmap", size=12)
plt.savefig('My_HEATMAP.jpg', bbox_inches='tight')
plt.close()  # Close the figure to free memory