# 分组统计分析

## 适用场景

将数据按某个类别字段分组，计算各组指标并进行对比。适用于：

- **质量检测**：按品种/批次/产地统计阳性率、合格率
- **市场分析**：按区域/渠道统计销售额、转化率
- **实验对比**：不同处理组的效果比较
- **任何需要"按类别看差异"的场景**

## 核心函数

### `group_analyze(df, group_col, metric_col=None, agg_funcs=None)`
通用分组聚合。自动计算各组计数、均值等。

```python
from scripts.analysis.group_analysis import group_analyze

# 按区域统计销售额
result = group_analyze(df, group_col="区域", metric_col="销售额",
                       agg_funcs={"销售额": ["count", "mean", "sum", "std"]})
```

### `group_rate_analysis(df, group_col, result_col, positive_val, value_col=None)`
率指标分析。自动计算各组的正例数、总数、率。

```python
from scripts.analysis.group_analysis import group_rate_analysis

# 按批次计算合格率
result = group_rate_analysis(df, group_col="批次", 
                             result_col="检测结论", positive_val="合格")
```

### `group_compare_plot(result_df, group_col, value_col, title="分组对比", plot_type="bar")`
分组对比可视化。支持柱状图和饼图。

```python
from scripts.analysis.group_analysis import group_compare_plot

fig = group_compare_plot(result, "品种", "阳性率", plot_type="bar")
```

### `generate_conclusion(result_df, group_col, value_col, higher_is_riskier=True)`
自动生成分析结论文本。

## 输出

1. **统计表** — 各组指标（计数、均值、率等）
2. **可视化** — 柱状图或饼图
3. **结论** — 最高/最低组、偏离程度、离散系数

## 数据要求

| 字段 | 类型 | 说明 |
|------|------|------|
| group_col | 任意 | 分类变量（字符串/整数） |
| metric_col | 数值 | 待统计的数值 |
| result_col | 二分类 | 用于率计算的二分类结果 |
