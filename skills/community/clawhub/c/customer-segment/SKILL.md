---
name: customer-segmentation
description: 金融客户分群分析 Skill。当用户上传银行客户数据表格（CSV/Excel）时自动触发，完成客户分层、特征提取和可视化输出。触发场景包括：（1）用户说"分析客户"或"客户分群"；（2）上传了包含客户交易、资产、行为等字段的数据文件；（3）需要输出客户分层结果、可视化图表或分群报告。
---

# Customer Segmentation Skill

金融客户分群分析：将客户按资产、交易行为、活跃度等维度进行分层，输出可操作的分群结果与可视化。

## 工作流程

### Step 1 — 数据加载与清洗

读取用户上传的 CSV 或 Excel 文件，自动识别列名。

优先保留字段：
- `customer_id` / `客户ID` — 客户唯一标识
- `age` / `年龄`
- `gender` / `性别`
- `balance` / `资产余额`
- `txn_amount` / `交易金额`
- `txn_count` / `交易次数`
- `last_date` / `最近交易日期`
- `product_count` / `持有产品数`
- `branch` / `网点`

缺失值处理：
- 数值型：用中位数填充
- 类别型：用众数填充
- 超过 30% 缺失的列：删除该列并提示用户

```python
import pandas as pd

df = pd.read_csv(file_path)
df.columns = df.columns.str.strip().str.lower()
```

### Step 2 — 特征工程

构建 RFM + 扩展特征：

| 特征 | 说明 |
|------|------|
| Recency | 距今天数（越小越活跃）|
| Frequency | 交易频率（指定周期内交易次数）|
| Monetary | 交易金额（指定周期内总金额）|
| Tenure | 客户持有时长（月）|
| Product_Depth | 持有产品数量 |
| Age | 客户年龄 |

数据标准化：使用 `StandardScaler`（Z-score）归一化所有数值型特征。

### Step 3 — 聚类分析

使用 **K-Means** 算法，自动确定 K 值（肘部法则 Elbow Method，SSE 拐点）。

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

# 肘部法则找最优K
sse = {}
for k in range(2, 10):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    sse[k] = km.inertia_
optimal_k = min(sse, key=sse.get)  # 简单取SSE最小的k
```

也可根据业务需求固定 K=5（高/中高/中/中低/低价值客户）。

### Step 4 — 分群画像

输出每个簇的核心统计量：

```
簇 0（高价值客户）：平均资产 85万，平均交易频次 28次/月，性别分布男62%
簇 1（潜力客户）：平均资产 32万，年轻化趋势明显
...
```

推荐标签体系（五类）：
- 🌟 高价值客户（VIP）
- ⬆️ 潜力客户
- 🟢 稳定客户
- 🔄 活跃交易客户
- ⚠️ 沉睡/流失预警客户

### Step 5 — 可视化

生成以下图表（保存为 PNG）：

1. **客户资产分布直方图** — 各层级资产分布对比
2. **雷达图** — 各分群特征对比
3. **热力图** — 分群特征均值矩阵
4. **散点图** — 以资产×交易频次为坐标的客户分布

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei']

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
# 资产分布
axes[0].hist([g['balance'] for _, g in df.groupby('cluster')], bins=30, label=[f'C{i}' for i in range(k)])
axes[0].set_title('Customer Balance Distribution by Cluster')
# 热力图
import seaborn as sns
sns.heatmap(cluster_means.T, annot=True, fmt='.1f', ax=axes[1])
axes[1].set_title('Cluster Feature Heatmap')
plt.tight_layout()
plt.savefig(output_path, dpi=150)
```

### Step 6 — 输出结果

输出内容：
1. 分群结果表（含客户ID、所属簇、分群标签）→ `segmentation_results.csv`
2. 分群特征统计 → `cluster_summary.csv`
3. 可视化图表 → `segmentation_charts.png`
4. 分析摘要（Markdown格式）→ `segmentation_report.md`

详细聚类和参数文档见：
- RFM 模型说明：参考 `references/rfm-guide.md`
- 聚类参数说明：参考 `references/clustering-guide.md`
