import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
%matplotlib inline
plt.style.use("ggplot")
def calculate_bin_counts(values, num_bins=10):
    """
    Calculate and print the count of values in each bin.
    Parameters:
    values (array-like): The data to bin.
    num_bins (int): Number of bins to use.
    Returns:
    np.ndarray: The original values.
    """
    values_array = np.array(values)
    bin_edges = np.linspace(values_array.min(), values_array.max(), num_bins + 1)
    bin_counts = {}
    for i in range(len(bin_edges) - 1):
        left_edge, right_edge = bin_edges[i], bin_edges[i+1]
        bin_label = f"({left_edge:.2f}, {right_edge:.2f}]"
        count = ((values_array > left_edge) & (values_array <= right_edge)).sum()
        bin_counts[bin_label] = count
    print(bin_counts)
    # Optional: get value counts from pandas cut
    bin_ranges = pd.cut(values_array, bins=bin_edges, precision=2).value_counts()
    # print(bin_ranges)  # Uncomment if needed
    return values_array
def plot_three_histograms(data_a, label_a, data_b, label_b, data_c, label_c, plot_title):
    """
    Plot histograms for three datasets on the same figure.
    Parameters:
    data_a, data_b, data_c (array-like): Data arrays.
    label_a, label_b, label_c (str): Labels for each dataset.
    plot_title (str): Title of the plot.
    """
    hist_params = {
        "bins": 40,
        "histtype": "stepfilled",
        "alpha": 0.5
    }
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.hist(data_a, label=label_a, **hist_params)
    ax.hist(data_b, label=label_b, **hist_params)
    ax.hist(data_c, label=label_c, **hist_params)
    ax.set_title(plot_title)
    fig.text(0.065, 0.5, 'Number of compounds', va='center', rotation='vertical', size=14)
    ax.legend()
    plt.show()