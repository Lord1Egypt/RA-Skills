---
name: cluster
version: "1.0.0"
description: "Perform data clustering analysis using k-means and hierarchical algorithms. Use when you need to group, classify, or segment datasets."
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags: [data, clustering, analysis, machine-learning, k-means, segmentation]
---

# Cluster — Data Clustering Analysis Tool

Cluster is a command-line data clustering analysis tool that supports k-means and hierarchical clustering algorithms. It reads numerical data from CSV/JSONL sources, performs clustering, evaluates cluster quality, and exports results.

Data is stored in `~/.cluster/data.jsonl` as JSONL records. Each record represents a clustering run with its parameters, assignments, centroids, and evaluation metrics.

## Prerequisites

- Python 3.8+ with standard library (no external packages required for basic operations)
- `bash` shell

## Commands

### `run`
Run a clustering algorithm on input data.

**Environment Variables:**
- `INPUT` (required) — Path to input CSV/JSONL file with numerical data
- `K` — Number of clusters (default: 3)
- `ALGORITHM` — Algorithm to use: `kmeans` or `hierarchical` (default: kmeans)
- `MAX_ITER` — Maximum iterations for k-means (default: 100)
- `SEED` — Random seed for reproducibility

**Example:**
```bash
INPUT=/path/to/data.csv K=5 ALGORITHM=kmeans bash scripts/script.sh run
```

### `assign`
Assign new data points to existing clusters from a previous run.

**Environment Variables:**
- `RUN_ID` (required) — ID of the clustering run to use
- `INPUT` (required) — Path to new data points (CSV/JSONL)

**Example:**
```bash
RUN_ID=abc123 INPUT=/path/to/new_data.csv bash scripts/script.sh assign
```

### `centroids`
Display or export centroid coordinates for a clustering run.

**Environment Variables:**
- `RUN_ID` (required) — ID of the clustering run
- `FORMAT` — Output format: `table`, `json`, `csv` (default: table)

### `evaluate`
Evaluate clustering quality with silhouette score, inertia, and Davies-Bouldin index.

**Environment Variables:**
- `RUN_ID` (required) — ID of the clustering run to evaluate

### `visualize`
Generate a text-based or ASCII visualization of cluster assignments.

**Environment Variables:**
- `RUN_ID` (required) — ID of the clustering run
- `DIMS` — Dimensions to plot, comma-separated (default: first two)

### `export`
Export clustering results to a file.

**Environment Variables:**
- `RUN_ID` (required) — ID of the run to export
- `OUTPUT` — Output file path (default: stdout)
- `FORMAT` — Export format: `json`, `csv`, `jsonl` (default: json)

### `import`
Import a previously exported clustering run.

**Environment Variables:**
- `INPUT` (required) — Path to the file to import

### `config`
View or update configuration settings.

**Environment Variables:**
- `KEY` — Configuration key to set
- `VALUE` — Configuration value

### `list`
List all stored clustering runs with summary info.

**Environment Variables:**
- `LIMIT` — Maximum runs to display (default: 20)
- `SORT` — Sort field: `date`, `k`, `score` (default: date)

### `stats`
Show aggregate statistics across all clustering runs.

### `help`
Display usage information and available commands.

### `version`
Display the current version of the cluster tool.

## Data Storage

All clustering runs are stored in `~/.cluster/data.jsonl`. Each line is a JSON object with fields:
- `id` — Unique run identifier
- `timestamp` — ISO 8601 creation time
- `algorithm` — Algorithm used
- `k` — Number of clusters
- `centroids` — List of centroid coordinates
- `assignments` — Mapping of data point indices to cluster IDs
- `metrics` — Evaluation metrics (silhouette, inertia, etc.)
- `input_file` — Source data file path
- `num_points` — Number of data points clustered

## Configuration

Config is stored in `~/.cluster/config.json`. Available keys:
- `default_k` — Default number of clusters (default: 3)
- `default_algorithm` — Default algorithm (default: kmeans)
- `max_iterations` — Default max iterations (default: 100)
- `random_seed` — Default random seed (default: 42)

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
