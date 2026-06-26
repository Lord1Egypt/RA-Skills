# 聚类分析参数参考

## 算法选择

| 算法 | 适用场景 | 优点 | 缺点 |
|------|----------|------|------|
| K-Means | 大数据集，簇近似球形 | 快速、可解释 | 对噪声/离群点敏感 |
| DBSCAN | 非凸簇，噪声检测 | 无需指定K，抗噪声 | 参数敏感，大数据慢 |
| 层次聚类 | 小数据，可解释层次 | 无需指定K，可画树状图 | O(n²)复杂度 |
| GMM | 簇大小/密度不同 | 软聚类（概率） | 需指定K，速度慢 |

**推荐银行客户分群用 K-Means**（大客户量，高效易解释）。

## K-Means 参数

```python
from sklearn.cluster import KMeans

km = KMeans(
    n_clusters=5,        # 聚类数（建议5-6）
    init='k-means++',      # 初始化方式（推荐，默认更优）
    n_init=10,             # 用不同初始化运行次数，取最优
    max_iter=300,          # 最大迭代次数
    random_state=42        # 随机种子（保证可复现）
)
```

## 最优K的选择

### 肘部法则（Elbow Method）

```python
import matplotlib.pyplot as plt

sse = {}
for k in range(2, 11):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    sse[k] = km.inertia_  # SSE（簇内误差平方和）

plt.plot(list(sse.keys()), list(sse.values()), 'bo-')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('SSE')
plt.title('Elbow Method for Optimal k')
plt.savefig('elbow_plot.png')
```

找"肘部"拐点（曲线变缓处）。

### 轮廓系数（Silhouette Score）

```python
from sklearn.metrics import silhouette_score

for k in range(2, 11):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    print(f"k={k}: silhouette={score:.3f}")
```

轮廓系数范围 [-1, 1]，越接近1越好。通常选 >0.4 的最大K。

## 特征预处理

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Z-score 标准化（推荐，对异常值相对稳健）
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# MinMax 缩放（对有界特征如转化率有效）
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
```

**重要：** K-Means 对量纲敏感，所有特征必须标准化。

## 分群结果评估

| 指标 | 计算方式 | 目标值 |
|------|----------|--------|
| 簇内 SSE | km.inertia_ | 越小越好 |
| 轮廓系数 | silhouette_score | >0.4 为可接受 |
| Davies-Bouldin | davies_bouldin_score | 越小越好（<1理想）|
| Calinski-Harabasz | calinski_harabasz_score | 越大越好 |

## 常见问题

**Q: 某些簇太大/太小怎么办？**
→ 可能是特征选择问题，尝试增加特征或对大类再细分（两层分群）。

**Q: 分群结果不稳定？**
→ 增加 `n_init` 至 20-50，或用层次聚类结果初始化 K-Means。

**Q: 离群点干扰？**
→ 聚类前先删除或标记离群点（DBSCAN 或 IQR 过滤）。
