#!/usr/bin/env bash
# Cluster — Data Clustering Analysis Tool
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
set -euo pipefail

DATA_DIR="$HOME/.cluster"
DATA_FILE="$DATA_DIR/data.jsonl"
CONFIG_FILE="$DATA_DIR/config.json"
VERSION="1.0.0"

mkdir -p "$DATA_DIR"
touch "$DATA_FILE"

if [ ! -f "$CONFIG_FILE" ]; then
  cat > "$CONFIG_FILE" << 'EOF'
{"default_k": 3, "default_algorithm": "kmeans", "max_iterations": 100, "random_seed": 42}
EOF
fi

COMMAND="${1:-help}"

case "$COMMAND" in
  run)
    python3 << 'PYEOF'
import os, json, csv, random, math, uuid, sys
from datetime import datetime

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.cluster/data.jsonl"))
config_file = os.environ.get("CONFIG_FILE", os.path.expanduser("~/.cluster/config.json"))
input_path = os.environ.get("INPUT", "")
k = int(os.environ.get("K", "3"))
algorithm = os.environ.get("ALGORITHM", "kmeans")
max_iter = int(os.environ.get("MAX_ITER", "100"))
seed = int(os.environ.get("SEED", "42"))

if not input_path:
    print("ERROR: INPUT environment variable is required")
    print("Usage: INPUT=/path/to/data.csv K=5 bash scripts/script.sh run")
    sys.exit(1)

# Load config defaults
try:
    with open(config_file) as f:
        cfg = json.load(f)
    if "K" not in os.environ:
        k = cfg.get("default_k", 3)
    if "ALGORITHM" not in os.environ:
        algorithm = cfg.get("default_algorithm", "kmeans")
    if "MAX_ITER" not in os.environ:
        max_iter = cfg.get("max_iterations", 100)
    if "SEED" not in os.environ:
        seed = cfg.get("random_seed", 42)
except:
    pass

# Read data from CSV or JSONL
data_points = []
try:
    if input_path.endswith(".jsonl"):
        with open(input_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    rec = json.loads(line)
                    if isinstance(rec, list):
                        data_points.append([float(x) for x in rec])
                    elif isinstance(rec, dict) and "features" in rec:
                        data_points.append([float(x) for x in rec["features"]])
                    elif isinstance(rec, dict):
                        vals = [v for v in rec.values() if isinstance(v, (int, float))]
                        data_points.append(vals)
    else:
        with open(input_path) as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                try:
                    data_points.append([float(x) for x in row])
                except ValueError:
                    nums = []
                    for x in row:
                        try:
                            nums.append(float(x))
                        except ValueError:
                            pass
                    if nums:
                        data_points.append(nums)
except FileNotFoundError:
    print(f"ERROR: File not found: {input_path}")
    sys.exit(1)

if not data_points:
    print("ERROR: No numeric data found in input file")
    sys.exit(1)

n_dims = len(data_points[0])
n_points = len(data_points)

print(f"Loaded {n_points} data points with {n_dims} dimensions")
print(f"Algorithm: {algorithm}, K: {k}, Max iterations: {max_iter}")

random.seed(seed)

def euclidean_dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def mean_point(points):
    if not points:
        return [0.0] * n_dims
    n = len(points)
    return [sum(p[d] for p in points) / n for d in range(len(points[0]))]

if algorithm == "kmeans":
    # K-means clustering
    indices = random.sample(range(n_points), min(k, n_points))
    centroids = [data_points[i][:] for i in indices]
    assignments = [0] * n_points

    for iteration in range(max_iter):
        # Assign points to nearest centroid
        new_assignments = []
        for point in data_points:
            dists = [euclidean_dist(point, c) for c in centroids]
            new_assignments.append(dists.index(min(dists)))

        if new_assignments == assignments and iteration > 0:
            print(f"Converged at iteration {iteration}")
            break
        assignments = new_assignments

        # Update centroids
        for j in range(k):
            cluster_points = [data_points[i] for i in range(n_points) if assignments[i] == j]
            if cluster_points:
                centroids[j] = mean_point(cluster_points)

    print(f"Completed {min(iteration + 1, max_iter)} iterations")
else:
    # Simple hierarchical clustering (agglomerative)
    clusters = {i: [i] for i in range(n_points)}
    assignments = list(range(n_points))
    centroids_map = {i: data_points[i][:] for i in range(n_points)}

    while len(clusters) > k:
        # Find closest pair of clusters
        min_dist = float("inf")
        merge_a, merge_b = -1, -1
        cluster_ids = list(clusters.keys())
        for i_idx in range(len(cluster_ids)):
            for j_idx in range(i_idx + 1, len(cluster_ids)):
                ci, cj = cluster_ids[i_idx], cluster_ids[j_idx]
                d = euclidean_dist(centroids_map[ci], centroids_map[cj])
                if d < min_dist:
                    min_dist = d
                    merge_a, merge_b = ci, cj

        # Merge clusters
        clusters[merge_a].extend(clusters[merge_b])
        combined = [data_points[i] for i in clusters[merge_a]]
        centroids_map[merge_a] = mean_point(combined)
        del clusters[merge_b]
        del centroids_map[merge_b]

    # Build final assignments
    final_clusters = list(clusters.keys())
    centroids = [centroids_map[c] for c in final_clusters]
    for idx, cid in enumerate(final_clusters):
        for pt_idx in clusters[cid]:
            assignments[pt_idx] = idx

    print(f"Hierarchical clustering complete with {k} clusters")

# Calculate inertia
inertia = 0.0
for i in range(n_points):
    inertia += euclidean_dist(data_points[i], centroids[assignments[i]]) ** 2

# Cluster sizes
sizes = {}
for a in assignments:
    sizes[a] = sizes.get(a, 0) + 1

# Calculate silhouette score (simplified)
silhouette_scores = []
for i in range(n_points):
    own_cluster = [j for j in range(n_points) if assignments[j] == assignments[i] and j != i]
    if not own_cluster:
        silhouette_scores.append(0.0)
        continue
    a_dist = sum(euclidean_dist(data_points[i], data_points[j]) for j in own_cluster) / len(own_cluster)
    b_dist = float("inf")
    for c in range(k):
        if c != assignments[i]:
            other = [j for j in range(n_points) if assignments[j] == c]
            if other:
                avg_d = sum(euclidean_dist(data_points[i], data_points[j]) for j in other) / len(other)
                b_dist = min(b_dist, avg_d)
    if b_dist == float("inf"):
        b_dist = 0
    s = (b_dist - a_dist) / max(a_dist, b_dist) if max(a_dist, b_dist) > 0 else 0
    silhouette_scores.append(s)

avg_silhouette = sum(silhouette_scores) / len(silhouette_scores) if silhouette_scores else 0

run_id = uuid.uuid4().hex[:12]
record = {
    "id": run_id,
    "timestamp": datetime.now().isoformat(),
    "algorithm": algorithm,
    "k": k,
    "centroids": [[round(v, 6) for v in c] for c in centroids],
    "assignments": assignments,
    "metrics": {
        "inertia": round(inertia, 4),
        "silhouette_score": round(avg_silhouette, 4),
        "cluster_sizes": sizes
    },
    "input_file": input_path,
    "num_points": n_points,
    "num_dims": n_dims,
    "max_iter": max_iter,
    "seed": seed
}

with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")

print(f"\nRun ID: {run_id}")
print(f"Clusters: {k}")
print(f"Inertia: {round(inertia, 4)}")
print(f"Silhouette Score: {round(avg_silhouette, 4)}")
print(f"\nCluster sizes:")
for c_id in sorted(sizes.keys()):
    print(f"  Cluster {c_id}: {sizes[c_id]} points")
print(f"\nResults saved to {data_file}")
PYEOF
    ;;

  assign)
    python3 << 'PYEOF'
import os, json, math, sys

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.cluster/data.jsonl"))
run_id = os.environ.get("RUN_ID", "")
input_path = os.environ.get("INPUT", "")

if not run_id:
    print("ERROR: RUN_ID environment variable is required")
    sys.exit(1)
if not input_path:
    print("ERROR: INPUT environment variable is required")
    sys.exit(1)

# Find the run
run_data = None
with open(data_file) as f:
    for line in f:
        line = line.strip()
        if line:
            rec = json.loads(line)
            if rec.get("id") == run_id:
                run_data = rec
                break

if not run_data:
    print(f"ERROR: Run ID '{run_id}' not found")
    sys.exit(1)

centroids = run_data["centroids"]

def euclidean_dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

# Read new data
import csv
new_points = []
try:
    if input_path.endswith(".jsonl"):
        with open(input_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    rec = json.loads(line)
                    if isinstance(rec, list):
                        new_points.append([float(x) for x in rec])
                    elif isinstance(rec, dict) and "features" in rec:
                        new_points.append([float(x) for x in rec["features"]])
    else:
        with open(input_path) as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                try:
                    new_points.append([float(x) for x in row])
                except ValueError:
                    pass
except FileNotFoundError:
    print(f"ERROR: File not found: {input_path}")
    sys.exit(1)

print(f"Assigning {len(new_points)} points to clusters from run {run_id}")
print(f"Using {len(centroids)} centroids\n")

for i, point in enumerate(new_points):
    dists = [euclidean_dist(point, c) for c in centroids]
    cluster = dists.index(min(dists))
    dist = min(dists)
    print(f"Point {i}: Cluster {cluster} (distance: {round(dist, 4)})")
PYEOF
    ;;

  centroids)
    python3 << 'PYEOF'
import os, json, sys

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.cluster/data.jsonl"))
run_id = os.environ.get("RUN_ID", "")
fmt = os.environ.get("FORMAT", "table")

if not run_id:
    print("ERROR: RUN_ID environment variable is required")
    sys.exit(1)

run_data = None
with open(data_file) as f:
    for line in f:
        line = line.strip()
        if line:
            rec = json.loads(line)
            if rec.get("id") == run_id:
                run_data = rec
                break

if not run_data:
    print(f"ERROR: Run ID '{run_id}' not found")
    sys.exit(1)

centroids = run_data["centroids"]

if fmt == "json":
    print(json.dumps(centroids, indent=2))
elif fmt == "csv":
    n_dims = len(centroids[0]) if centroids else 0
    header = ",".join([f"dim_{i}" for i in range(n_dims)])
    print(f"cluster,{header}")
    for i, c in enumerate(centroids):
        vals = ",".join([str(v) for v in c])
        print(f"{i},{vals}")
else:
    print(f"Centroids for run {run_id}:")
    print(f"{'Cluster':<10} {'Coordinates'}")
    print("-" * 60)
    for i, c in enumerate(centroids):
        coords = ", ".join([f"{v:.4f}" for v in c])
        print(f"{i:<10} [{coords}]")
PYEOF
    ;;

  evaluate)
    python3 << 'PYEOF'
import os, json, math, sys

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.cluster/data.jsonl"))
run_id = os.environ.get("RUN_ID", "")

if not run_id:
    print("ERROR: RUN_ID environment variable is required")
    sys.exit(1)

run_data = None
with open(data_file) as f:
    for line in f:
        line = line.strip()
        if line:
            rec = json.loads(line)
            if rec.get("id") == run_id:
                run_data = rec
                break

if not run_data:
    print(f"ERROR: Run ID '{run_id}' not found")
    sys.exit(1)

metrics = run_data.get("metrics", {})
print(f"Evaluation metrics for run {run_id}:")
print(f"{'='*50}")
print(f"Algorithm:        {run_data.get('algorithm', 'unknown')}")
print(f"K (clusters):     {run_data.get('k', 'unknown')}")
print(f"Data points:      {run_data.get('num_points', 'unknown')}")
print(f"Dimensions:       {run_data.get('num_dims', 'unknown')}")
print(f"{'='*50}")
print(f"Inertia (SSE):    {metrics.get('inertia', 'N/A')}")
print(f"Silhouette Score: {metrics.get('silhouette_score', 'N/A')}")

sizes = metrics.get("cluster_sizes", {})
if sizes:
    print(f"\nCluster Distribution:")
    total = sum(sizes.values())
    for cid in sorted(sizes.keys(), key=lambda x: int(x)):
        pct = (sizes[cid] / total * 100) if total > 0 else 0
        bar = "█" * int(pct / 2)
        print(f"  Cluster {cid}: {sizes[cid]:>5} ({pct:.1f}%) {bar}")
PYEOF
    ;;

  visualize)
    python3 << 'PYEOF'
import os, json, sys

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.cluster/data.jsonl"))
run_id = os.environ.get("RUN_ID", "")
dims_str = os.environ.get("DIMS", "0,1")

if not run_id:
    print("ERROR: RUN_ID environment variable is required")
    sys.exit(1)

run_data = None
with open(data_file) as f:
    for line in f:
        line = line.strip()
        if line:
            rec = json.loads(line)
            if rec.get("id") == run_id:
                run_data = rec
                break

if not run_data:
    print(f"ERROR: Run ID '{run_id}' not found")
    sys.exit(1)

centroids = run_data["centroids"]
assignments = run_data["assignments"]
k = run_data["k"]

# We'll create a simple text-based visualization showing cluster distribution
symbols = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

print(f"Cluster Visualization for run {run_id}")
print(f"{'='*50}")

# Cluster size bar chart
sizes = {}
for a in assignments:
    sizes[a] = sizes.get(a, 0) + 1

max_size = max(sizes.values()) if sizes else 1
bar_width = 40

print(f"\nCluster Size Distribution:")
print(f"{'Cluster':<10} {'Size':>6} {'Bar'}")
print("-" * 60)
for c in sorted(sizes.keys()):
    bar_len = int((sizes[c] / max_size) * bar_width)
    sym = symbols[c % len(symbols)]
    bar = sym * bar_len
    print(f"  {c:<8} {sizes[c]:>6} |{bar}")

# Centroid distances matrix
print(f"\nInter-centroid Distances:")
if len(centroids) > 1:
    import math
    header = "      " + "".join([f"  C{i:<4}" for i in range(len(centroids))])
    print(header)
    for i in range(len(centroids)):
        row = f"C{i:<4} "
        for j in range(len(centroids)):
            d = math.sqrt(sum((a - b) ** 2 for a, b in zip(centroids[i], centroids[j])))
            row += f"{d:>6.2f} "
        print(row)
PYEOF
    ;;

  export)
    python3 << 'PYEOF'
import os, json, sys

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.cluster/data.jsonl"))
run_id = os.environ.get("RUN_ID", "")
output = os.environ.get("OUTPUT", "")
fmt = os.environ.get("FORMAT", "json")

if not run_id:
    print("ERROR: RUN_ID environment variable is required")
    sys.exit(1)

run_data = None
with open(data_file) as f:
    for line in f:
        line = line.strip()
        if line:
            rec = json.loads(line)
            if rec.get("id") == run_id:
                run_data = rec
                break

if not run_data:
    print(f"ERROR: Run ID '{run_id}' not found")
    sys.exit(1)

if fmt == "json":
    result = json.dumps(run_data, indent=2)
elif fmt == "csv":
    lines = ["point_index,cluster_id"]
    for i, a in enumerate(run_data.get("assignments", [])):
        lines.append(f"{i},{a}")
    result = "\n".join(lines)
elif fmt == "jsonl":
    result = json.dumps(run_data)
else:
    result = json.dumps(run_data, indent=2)

if output:
    with open(output, "w") as f:
        f.write(result + "\n")
    print(f"Exported run {run_id} to {output} ({fmt} format)")
else:
    print(result)
PYEOF
    ;;

  import)
    python3 << 'PYEOF'
import os, json, sys

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.cluster/data.jsonl"))
input_path = os.environ.get("INPUT", "")

if not input_path:
    print("ERROR: INPUT environment variable is required")
    sys.exit(1)

try:
    with open(input_path) as f:
        content = f.read().strip()
except FileNotFoundError:
    print(f"ERROR: File not found: {input_path}")
    sys.exit(1)

try:
    data = json.loads(content)
except json.JSONDecodeError:
    # Try JSONL
    lines = content.split("\n")
    for line in lines:
        line = line.strip()
        if line:
            try:
                data = json.loads(line)
                with open(data_file, "a") as f:
                    f.write(json.dumps(data) + "\n")
            except:
                pass
    print(f"Imported data from {input_path}")
    sys.exit(0)

if isinstance(data, list):
    count = 0
    for item in data:
        with open(data_file, "a") as f:
            f.write(json.dumps(item) + "\n")
        count += 1
    print(f"Imported {count} records from {input_path}")
else:
    with open(data_file, "a") as f:
        f.write(json.dumps(data) + "\n")
    print(f"Imported 1 record from {input_path}")
    print(f"Run ID: {data.get('id', 'unknown')}")
PYEOF
    ;;

  config)
    python3 << 'PYEOF'
import os, json, sys

config_file = os.environ.get("CONFIG_FILE", os.path.expanduser("~/.cluster/config.json"))
key = os.environ.get("KEY", "")
value = os.environ.get("VALUE", "")

try:
    with open(config_file) as f:
        cfg = json.load(f)
except:
    cfg = {"default_k": 3, "default_algorithm": "kmeans", "max_iterations": 100, "random_seed": 42}

if key and value:
    # Try to convert to appropriate type
    try:
        value = int(value)
    except ValueError:
        try:
            value = float(value)
        except ValueError:
            if value.lower() in ("true", "false"):
                value = value.lower() == "true"
    cfg[key] = value
    with open(config_file, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"Set {key} = {value}")
elif key:
    if key in cfg:
        print(f"{key} = {cfg[key]}")
    else:
        print(f"Unknown config key: {key}")
        print(f"Available keys: {', '.join(cfg.keys())}")
else:
    print("Current configuration:")
    print(json.dumps(cfg, indent=2))
PYEOF
    ;;

  list)
    python3 << 'PYEOF'
import os, json, sys

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.cluster/data.jsonl"))
limit = int(os.environ.get("LIMIT", "20"))
sort_by = os.environ.get("SORT", "date")

runs = []
try:
    with open(data_file) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    runs.append(json.loads(line))
                except:
                    pass
except FileNotFoundError:
    pass

if not runs:
    print("No clustering runs found.")
    print("Use 'run' command to create a new clustering run.")
    sys.exit(0)

if sort_by == "k":
    runs.sort(key=lambda x: x.get("k", 0))
elif sort_by == "score":
    runs.sort(key=lambda x: x.get("metrics", {}).get("silhouette_score", 0), reverse=True)
else:
    runs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

runs = runs[:limit]

print(f"{'ID':<14} {'Date':<20} {'Algorithm':<12} {'K':>3} {'Points':>7} {'Silhouette':>11} {'Inertia':>10}")
print("-" * 80)
for r in runs:
    ts = r.get("timestamp", "")[:19]
    algo = r.get("algorithm", "?")
    k = r.get("k", "?")
    pts = r.get("num_points", "?")
    sil = r.get("metrics", {}).get("silhouette_score", "N/A")
    iner = r.get("metrics", {}).get("inertia", "N/A")
    sil_str = f"{sil:.4f}" if isinstance(sil, (int, float)) else str(sil)
    iner_str = f"{iner:.2f}" if isinstance(iner, (int, float)) else str(iner)
    print(f"{r.get('id', '?'):<14} {ts:<20} {algo:<12} {k:>3} {pts:>7} {sil_str:>11} {iner_str:>10}")

print(f"\nTotal: {len(runs)} runs shown")
PYEOF
    ;;

  stats)
    python3 << 'PYEOF'
import os, json, sys

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.cluster/data.jsonl"))

runs = []
try:
    with open(data_file) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    runs.append(json.loads(line))
                except:
                    pass
except FileNotFoundError:
    pass

if not runs:
    print("No clustering runs found.")
    sys.exit(0)

total_runs = len(runs)
algos = {}
k_values = []
silhouettes = []
total_points = 0

for r in runs:
    algo = r.get("algorithm", "unknown")
    algos[algo] = algos.get(algo, 0) + 1
    k_values.append(r.get("k", 0))
    total_points += r.get("num_points", 0)
    sil = r.get("metrics", {}).get("silhouette_score")
    if isinstance(sil, (int, float)):
        silhouettes.append(sil)

print(f"Cluster Analysis Statistics")
print(f"{'='*50}")
print(f"Total runs:           {total_runs}")
print(f"Total points analyzed:{total_points}")
print(f"\nAlgorithm usage:")
for algo, count in sorted(algos.items()):
    print(f"  {algo}: {count} runs")
print(f"\nK values:")
if k_values:
    print(f"  Min: {min(k_values)}")
    print(f"  Max: {max(k_values)}")
    print(f"  Avg: {sum(k_values)/len(k_values):.1f}")
if silhouettes:
    print(f"\nSilhouette scores:")
    print(f"  Min:  {min(silhouettes):.4f}")
    print(f"  Max:  {max(silhouettes):.4f}")
    print(f"  Mean: {sum(silhouettes)/len(silhouettes):.4f}")
    best = runs[silhouettes.index(max(silhouettes))]
    print(f"  Best run: {best.get('id', '?')} (score: {max(silhouettes):.4f})")
PYEOF
    ;;

  help)
    cat << 'HELPEOF'
Cluster — Data Clustering Analysis Tool v1.0.0

Usage: bash scripts/script.sh <command>

Commands:
  run         Run clustering algorithm on input data
  assign      Assign new data points to existing clusters
  centroids   Display centroid coordinates
  evaluate    Evaluate clustering quality metrics
  visualize   Generate text-based cluster visualization
  export      Export clustering results
  import      Import previously exported runs
  config      View/update configuration
  list        List all clustering runs
  stats       Show aggregate statistics
  help        Show this help message
  version     Show version

Environment Variables:
  INPUT       Input data file path (CSV or JSONL)
  K           Number of clusters (default: 3)
  ALGORITHM   kmeans or hierarchical (default: kmeans)
  RUN_ID      ID of a specific clustering run
  FORMAT      Output format (json, csv, table)

Examples:
  INPUT=data.csv K=5 bash scripts/script.sh run
  RUN_ID=abc123 bash scripts/script.sh centroids
  RUN_ID=abc123 FORMAT=csv bash scripts/script.sh export

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
HELPEOF
    ;;

  version)
    echo "cluster v${VERSION}"
    ;;

  *)
    echo "Unknown command: $COMMAND"
    echo "Run 'bash scripts/script.sh help' for usage information"
    exit 1
    ;;
esac
