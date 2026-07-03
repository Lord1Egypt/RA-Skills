# ANOVA方差分析

## 适用场景

比较多个组（>2组）的均值是否存在统计显著差异。

- **批次间比对**：不同批次的检测结果是否一致
- **实验室间比对**：不同实验室的检测结果是否有系统性差异
- **处理效果比较**：多个处理组的均值差异
- **工艺参数优化**：不同参数配置下的效果差异

## 核心函数

### `anova_oneway(groups)`
单因素方差分析。

```python
from scripts.analysis.anova import anova_oneway

# 按名称传入
groups = {
    "实验室A": [12.6, 8.3, 8.21],
    "实验室B": [19.5, 17.2, 13.77],
    "实验室C": [24.2, 18.85, 18.39],
}
result = anova_oneway(groups)

# 或按顺序传入
groups = [[12.6, 8.3, 8.21], [19.5, 17.2, 13.77]]
result = anova_oneway(groups)
```

### `anova_table(result)`
将ANOVA结果格式化为 pandas DataFrame。

```python
from scripts.analysis.anova import anova_table

df_table = anova_table(result)
```

### `f_critical(df1, df2, alpha=0.05)`
F临界值查表（α=0.05）。

```python
from scripts.analysis.anova import f_critical

fc = f_critical(2, 6)  # → 5.14
```

## 输出

```text
ANOVA 方差分析表
============================================================
变异来源     SS           df       MS          F           显著性
------------------------------------------------------------
组间(SSB)    XX.XXXX     2        XX.XXXX     X.XXXX       √
组内(SSW)    XX.XXXX     6        XX.XXXX
总变异(SST)  XX.XXXX     8
------------------------------------------------------------
F临界值(α=0.05): F(2, 6) = 5.1433
结论: 各组均值存在显著差异 / 各组均值无显著差异
```

返回结果结构:

| 字段 | 说明 |
|------|------|
| `ssb` / `ssw` / `sst` | 组间/组内/总平方和 |
| `dfb` / `dfw` / `dft` | 自由度 |
| `msb` / `msw` | 组间/组内均方 |
| `f_value` | F统计量 |
| `f_critical` | F临界值(α=0.05) |
| `significant` | 是否显著(bool) |
| `group_means` | 各组均值 |
| `grand_mean` | 总均值 |
| `table` | 格式化文本表 |

## 数据要求

- 各组数据长度可以不同
- 数据应为数值型
- 建议每组至少3个数据点
- 数据应近似正态分布、方差齐性

## F临界值表覆盖范围

| 分子自由度(dfb) | 1-8, 12, 24 |
| 分母自由度(dfw) | 1-20 |
| 显著性水平 | α=0.05 |

分子自由度超过24时取24近似，分母自由度超过20时取20近似。
