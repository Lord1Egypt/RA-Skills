# Clustering Analysis Parameter Reference

## Algorithm Selection

| Algorithm | Applicable Scenario | Advantages | Disadvantages |
|-----------|---------------------|------------|---------------|
| K-Means | Large datasets, approximately spherical clusters | Fast, interpretable | Sensitive to noise/outliers |
| DBSCAN | Non-convex clusters, noise detection | No need to specify K, noise-resistant | Parameter-sensitive, slow on large data |
| Hierarchical Clustering | Small data, interpretable hierarchy | No need to specify K, dendrogram possible | O(n²) complexity |
| GMM | Clusters with different sizes/densities | Soft clustering (probabilistic) | Need to specify K, slow |

**K-Means is recommended for bank customer segmentation** (large customer volume, efficient and interpretable).

## K-Means Parameters

```python
from sklearn.cluster import KMeans

km = KMeans(
    n_clusters=5,        # Number of clusters (recommended 5-6)
    init='k-means++',      # Initialization method (recommended, better default)
    n_init=10,             # Number of runs with different initializations, take best
    max_iter=300,          # Maximum number of iterations
    random_state=42        # Random seed (ensure reproducibility)
)
```

## Optimal K Selection

### Elbow Method

```python
import matplotlib.pyplot as plt

sse = {}
for k in range(2, 11):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    sse[k] = km.inertia_  # SSE (sum of squared errors within clusters)

plt.plot(list(sse.keys()), list(sse.values()), 'bo-')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('SSE')
plt.title('Elbow Method for Optimal k')
plt.savefig('elbow_plot.png')
```

Find the "elbow" inflection point (where the curve flattens).

### Silhouette Score

```python
from sklearn.metrics import silhouette_score

for k in range(2, 11):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    print(f"k={k}: silhouette={score:.3f}")
```

Silhouette score ranges from [-1, 1], closer to 1 is better. Usually select the largest K with score >0.4.

## Feature Preprocessing

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Z-score standardization (recommended, relatively robust to outliers)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# MinMax scaling (effective for bounded features like conversion rates)
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
```

**Important:** K-Means is sensitive to scale, all features must be standardized.

## Segmentation Result Evaluation

| Metric | Calculation Method | Target Value |
|--------|-------------------|--------------|
| Within-Cluster SSE | km.inertia_ | Smaller is better |
| Silhouette Score | silhouette_score | >0.4 is acceptable |
| Davies-Bouldin | davies_bouldin_score | Smaller is better (<1 ideal) |
| Calinski-Harabasz | calinski_harabasz_score | Larger is better |

## Common Issues

**Q: What if some clusters are too large/small?**
→ May be a feature selection issue, try adding features or further subdividing large clusters (two-level clustering).

**Q: Segmentation results are unstable?**
→ Increase `n_init` to 20-50, or initialize K-Means with hierarchical clustering results.

**Q: Outliers interfering?**
→ Remove or flag outliers before clustering (DBSCAN or IQR filtering).