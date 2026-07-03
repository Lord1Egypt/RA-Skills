# PCA主成分分析

## 适用场景

多变量数据降维、结构发现、一致性评价。

- **多指标综合评价**：多个检测指标 → 少数主成分
- **数据降维可视化**：高维数据 → 2D/3D散点图
- **一致性评价**：不同方法/仪器检测结果的一致性判定
- **变量筛选**：识别贡献最大的变量

## 核心函数

### `pca_analyze(df, variance_threshold=0.95, n_components=None)`
完整PCA分析流程。

```python
from scripts.analysis.pca_analysis import pca_analyze

result = pca_analyze(df, variance_threshold=0.95)
# result["transformed"]  — 降维后数据
# result["components"]   — 主成分载荷
# result["explained_ratio"] — 方差贡献率
# result["cumulative_ratio"] — 累积贡献率
# result["n_selected"]   — 选定的主成分数
```

### `scree_plot(full_pca, threshold=0.95, highlight_k=None)`
碎石图（累积贡献率）。用于确定保留多少个主成分。

```python
from scripts.analysis.pca_analysis import scree_plot

fig = scree_plot(result["full_pca"], threshold=0.95)
```

### `pca_scatter(pca_result, labels=None, dim=2)`
主成分散点图。自动选择2D或3D。

```python
# 2D散点图
fig = pca_scatter(result, dim=2)

# 3D散点图（需要至少3个主成分）
fig = pca_scatter(result, dim=3)

# 带标签着色
fig = pca_scatter(result, labels=df["品种"], dim=2)
```

### `consistency_evaluation(df, threshold=0.9)`
一致性评价。计算成对变量的相关系数平方(R²)，与阈值比较判定。

```python
from scripts.analysis.pca_analysis import consistency_evaluation

eval_result = consistency_evaluation(df, threshold=0.9)
```

## 输出

| 输出 | 说明 |
|------|------|
| `transformed` | 降维后的主成分得分 |
| `factor_scores` | 标准化后的因子得分 |
| `components` | 载荷矩阵（变量对主成分的贡献） |
| `component_scores` | 成分得分系数矩阵 |
| `explained_ratio` | 各主成分方差贡献率 |
| 碎石图 | 确定主成分数量 |
| 散点图 | 样本在低维空间的分布 |
| 一致性评价表 | 成对变量的一致性判断 |

## 数据要求

- 行为样本，列为变量
- 变量应为数值型（自动标准化）
- 样本数 > 变量数时效果最佳
