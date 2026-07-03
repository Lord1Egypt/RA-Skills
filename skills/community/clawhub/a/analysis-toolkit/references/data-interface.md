# 数据接口规范

## 概述

所有场景函数的入参统一为以下三种类型之一，没有例外。

| 类型 | 表示 | 适用场景 |
|------|------|---------|
| **DataFrame** | `pd.DataFrame` | 多列结构化数据（原始检测记录、批量数据） |
| **array-like** | `list` / `np.ndarray` | 单维度数值序列（浓度、响应值、平行样结果） |
| **dict** | 前序函数的返回值 | 传递中间结果（calibration_data, 统计结果） |

## 一、DataFrame 类 —— 列名约定

所有场景函数通过**列名字符串参数**来指定数据列，不依赖固定列名。

### 参数重要性标注

从 v2 开始，接口文档使用以下标注明确区分参数类型：

| 标注 | 含义 | 示例 |
|------|------|------|
| **`[必填]`** | 必须提供，不填则抛 ValueError | `value_col[必填]` |
| **`[条件必填]`** | 特定场景下必须提供 | `reference[条件必填]`（总误差计算） |
| **`[可选]`** | 不提供则使用默认值 | `blank[可选]`（回收率计算） |
| **`[互斥]`** | 与另一个参数二选一 | `calibration_data` / `sigma+slope` |

### 关键场景的必填参数

| 场景 | 必填参数 | 条件必填 | 说明 |
|------|---------|---------|------|
| **总误差 (TE)** | `values[必填]`, `reference[必填]` | `t_crit`（不提供则自动查表） | reference 是参考值/真值/指定值 |
| **偏倚计算** | `values[必填]`, `reference[必填]` | — | 偏倚 = mean - reference |
| **不确定度评定** | `bias[必填]` / `values[必填]` | `distribution`（默认 normal） | 见各算子签名 |
| **Z 值分析** | `x[必填]`, `assigned_value[必填]`, `std_dev[必填]` | — | 三者缺一不可 |
| **LOD/LOQ** | `sigma[必填]` + `slope[必填]` 或 `calibration_data[必填]` | `standard`（默认 pharmacopoeia） | 互斥参数二选一 |
| **室内精密度** | `level_col[必填]`, `value_col[必填]` | — | 每水平至少 2 个数据点 |
| **室间比对 ANOVA** | `lab_col[必填]`, `value_col[必填]` | — | 每组至少 2 个数据点 |

---

| 参数名 | 数据类型 | 说明 | 典型列名示例 |
|--------|---------|------|-------------|
| `value_col` | float | 数值结果列（测量值、含量、浓度） | "结果", "浓度", "响应值", "含量", "测量值" |
| `group_col` | str / int | 分组标识列（类别、批次、实验室） | "品种", "批次", "实验室", "人员", "方法" |
| `date_col` | datetime64 | 日期时间列 | "日期", "检测日期", "分析日期", "采样日期" |
| `level_col` | str / int | 水平/浓度水平标识 | "水平", "浓度水平", "添加水平" |
| `lab_col` | str / int | 实验室/操作人员标识 | "实验室", "操作人", "检测人员" |
| `batch_col` | str / int | 批次标识 | "批次", "批号", "生产批次" |
| `result_col` | str (二分类) | 判定结果列 | "检测结果", "判定", "合格" |

### 数据质量要求

| 要求 | 说明 |
|------|------|
| **无空值** | 涉及分析的数值列不得有 NaN，有则自动跳过（警告） |
| **日期格式** | date_col 需为 `datetime64` 类型。字符串日期自动用 `pd.to_datetime()` 转换 |
| **数值列** | value_col 必须可转换为 float。非数值强制转换失败时抛 ValueError |
| **分组列** | group_col / lab_col / level_col 空值视为不同组 |

### 错误处理

所有函数遇到数据问题时抛标准 Python 异常：
- `ValueError` — 参数不合法、数据不符合要求
- `TypeError` — 类型不匹配
- `ImportError` — 缺少可选依赖（prophet）

不会静默返回 None 或空结果。

---

## 二、各场景的数据要求

### 场景 1：室内质控

#### internal_precision_analysis(data, level_col, value_col, n_replicates)

```
data 示例：
┌──────┬────────┐
│ 水平  │ 结果   │  ← level_col="水平", value_col="结果"
├──────┼────────┤
│ 1    │ 12.6   │
│ 1    │ 8.3    │
│ 1    │ 8.21   │
│ 2    │ 19.5   │
│ 2    │ 17.2   │
│ 2    │ 13.77  │
│ 3    │ 24.2   │
│ 3    │ 18.85  │
│ 3    │ 18.39  │
└──────┴────────┘

level_col: 每水平至少2行（建议3行）
value_col: 纯数值
n_replicates: 每水平预期的重复次数（用于校验）
```

#### repeatability_check(results, tolerance_pct)

```
results 示例：
[12.6, 8.3, 8.21]

纯数值列表，不涉及 DataFrame。
tolerance_pct: 可选，不提供则根据结果数量级自动查允许值表。
```

#### control_chart(data, value_col, date_col)

```
data 示例：
┌────────────┬────────┐
│ 日期       │ 结果   │  ← date_col="日期", value_col="结果"
├────────────┼────────┤
│ 2024-01-01 │ 50.2   │
│ 2024-01-02 │ 51.1   │
│ 2024-01-03 │ 49.8   │
│ ...        │ ...    │
└────────────┴────────┘

date_col: 可选。不提供时自动生成序号作为 X 轴。
value_col: 质控物的连续测量值，至少10个点以上。
```

---

### 场景 2：室间比对 / 批次比对

#### interlab_comparison(data, lab_col, value_col)

```
data 示例：
┌──────────┬────────┐
│ 实验室   │ 结果   │  ← lab_col="实验室", value_col="结果"
├──────────┼────────┤
│ 实验室A  │ 50.2   │
│ 实验室A  │ 51.0   │
│ 实验室A  │ 49.8   │
│ 实验室B  │ 53.1   │
│ 实验室B  │ 52.7   │
│ 实验室B  │ 53.4   │
│ ...      │ ...    │
└──────────┴────────┘

lab_col: 每个实验室至少2个数据点（建议3个以上）。
value_col: 纯数值。
```

#### z_score_analysis(data, lab_col, value_col)

与 interlab_comparison 相同的 DataFrame 结构。

可选参数 `assigned_value` 和 `std_dev`：
- 不提供时：指定值=所有数据中位数，SD=稳健标准差(MAD×1.4826)
- 提供时：直接使用传入值

#### youden_plot(data_a, data_b, label_a="实验室A", label_b="实验室B", title="Youden图 — 双实验室比对")

```
data_a = [50.2, 51.0, 49.8, ...]   ← 实验室A的各样本结果
data_b = [53.1, 52.7, 53.4, ...]   ← 实验室B的各样本结果

两个数组长度相同，每个位置对应同一个样本。
```

#### interbatch_analysis(data, batch_col, value_col)

与 interlab_comparison 相同的结构，只是列名不同：
```
lab_col   → batch_col  ("批次")
value_col → value_col  ("结果")
```

---

### 场景 3：方法验证

#### calibration_curve(x, y, force_zero, degree)

```
x = [0, 5, 10, 15, 20, 25]       ← 标准系列浓度（array-like）
y = [101, 32500, 66000, 91300, 133005, 162037]  ← 响应值/峰面积

force_zero: True=强制过原点, False=普通线性
degree: 1=线性, >1=多项式拟合
```

#### calc_lod_loq(sigma, slope, standard, sigma_source, calibration_data)

两种传参方式等价：

**方式A：直接给 sigma 和 slope**
```python
calc_lod_loq(sigma=0.05, slope=2.5, standard="gbt27417")
```

**方式B：传 calibration_data 自动提取**
```python
cal_data = calibration_curve(x, y)  # 得到 dict
calc_lod_loq(calibration_data=cal_data, standard="gbt27417")
# 自动用 cal_data["syx"] 和 cal_data["slope"]
```

sigma_source 取值：
| 值 | σ 来源 | 说明 |
|----|--------|------|
| `"curve"` | Sy/x（曲线回归剩余标准差） | 校准方程法，不需要额外数据 |
| `"instrument"` | 仪器精密度 SD | 需单独做仪器精密度试验 |
| `"blank"` | 空白测定 SD（n≥10） | 空白标准偏差法 |
| `"noise"` | 基线噪声 SD | 信噪比法，光谱类仪器 |

standard 取值：
| 值 | 公式 | 来源 |
|----|------|------|
| `"gbt27417"` | LOD=3σ/b, LOQ=3×LOD | GB/T 27417-2017 |
| `"ich"` | LOD=3.3σ/b, LOQ=10σ/b | ICH Q2(R1)/中国药典 |

#### calc_recovery(measured, spiked, blank)

```
measured = [95.2, 97.8, 93.5]      ← 加标样品测定值
spiked = 100                       ← 加标浓度（或数组 [100, 100, 100]）
blank = 0.5                        ← 空白值
```

#### curve_uncertainty(calibration_data, sample_responses, n_cal_points=None, n_sample_replicates=None)

```
calibration_data 来自 calibration_curve() 的返回值。
sample_responses = [0.6521, 0.6529, 0.6514]  ← 样品的多次测量响应值
```

---

### 场景 4：趋势监控

#### monitoring_dashboard(data, date_col, value_col, group_col, freq, window)

```
data 示例：
┌────────────┬────────┬────────┐
│ 日期       │ 值     │ 品种   │  ← date_col="日期", value_col="值"
├────────────┼────────┼────────┤
│ 2024-01-01 │ 50     │ 白菜   │
│ 2024-01-02 │ 55     │ 白菜   │
│ 2024-01-03 │ 48     │ 白菜   │
│ ...        │ ...    │ ...    │
└────────────┴────────┴────────┘

freq: "D"=日, "W"=周, "M"=月, "Q"=季度
window: 滚动窗口大小（默认7）
```

#### forecast_alert(data, date_col, value_col, group_col, freq, periods, alert_threshold)

与 monitoring_dashboard 相同的 DataFrame 结构。
```
periods: 预测期数（默认4）
alert_threshold: 预警阈值，预测增长率超过此值时发出警报（默认0.2=20%）
```

---

### 场景 5：分组分析 / PCA / 回归 / ANOVA

#### group_analyze(df, group_col, metric_col, agg_funcs)

```
df 示例：
┌────────┬────────┬────────┐
│ 品种   │ 结果   │ 数量   │  ← group_col="品种"
├────────┼────────┼────────┤
│ 白菜   │ 阳性   │ 100    │
│ 猪肉   │ 阴性   │ 200    │
│ ...    │ ...    │ ...    │
└────────┴────────┴────────┘

agg_funcs: 可选，自定义聚合函数 dict {列名: 函数}
```

#### pca_analyze(df, variance_threshold, n_components)

```
df 示例（纯数值，行=样本，列=变量）：
┌──────┬──────┬──────┬──────┐
│ 变量1 │ 变量2 │ 变量3 │ 变量4 │
├──────┼──────┼──────┼──────┤
│ 1.2  │ 3.4  │ 5.6  │ 7.8  │
│ 2.1  │ 4.3  │ 6.5  │ 8.7  │
│ ...  │ ...  │ ...  │ ...  │
└──────┴──────┴──────┴──────┘

自动 Z-score 标准化。不能有 NaN。
```

#### anova_oneway(groups)

```python
# dict 方式（推荐）
groups = {"组A": [50, 51, 49], "组B": [53, 52, 54], "组C": [48, 49, 50]}

# list 方式
groups = [[50, 51, 49], [53, 52, 54], [48, 49, 50]]
```

---

## 三、Pipeline 数据流

Pipeline 中步骤之间的数据传递通过引用语法实现：

```
%input%          → 整个原始输入（传给 run() 的那个值）
%步骤名%         → 该步骤的完整返回值（dict）
%步骤名.字段名%  → 返回值中的某个字段
```

例如方法验证模板：
```
输入: {"x": [...], "y": [...], "y_sample": [...]}
  ↓ %input.x%   %input.y%  ────────────┐
标准曲线拟合                               ↓ calibration_data
  ↓ %标准曲线%  ─────────────┐           │
  ↓                        ↓           ↓
LOD/LOQ  ←─ calc_lod_loq   曲线不确定度 ←─ curve_uncertainty
  ↓                        ↓
校准曲线图 ←─ calibration_plot
```

Pipeline 接受以下输入格式：

| 输入类型 | 示例 |
|---------|------|
| DataFrame | 直接传 df |
| dict | `{"x": [...], "y": [...], "y_sample": [...]}` （多组数据） |
| 单值 | 数值、字符串等单步场景 |

---

## 四、输出规范

所有场景函数返回 `dict`，包含以下标准字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| 统计量 | float / DataFrame | 核心计算结果 |
| fig | matplotlib Figure | 可视化图表（可选） |
| conclusion | str | 结论文本（可选） |
| warnings | list[str] | 数据质量警告列表（空列表=无问题）。当数据存在潜在问题（如含空值、列名不存在、标准差为0等）时，此处列出具体说明，避免静默返回错误结果。 |
| 其他 | 依函数而定 | 见各函数文档 |

图表统一为 `matplotlib.figure.Figure` 对象，可通过 `fig.savefig()` 导出为图片文件，或通过 `report.generate_report()` 嵌入 Word 报告。

---

## 五、快速参考：你要什么数据

| 你要做什么 | 需要什么数据 | 列/参数 |
|-----------|-------------|---------|
| 室内精密度分析 | DataFrame 多水平重复测量 | level_col="水平", value_col="结果" |
| 重复限性检查 | 数值列表（平行样） | results=[...] |
| 质控图 | DataFrame 连续测量值 | value_col="结果", date_col="日期"(可选) |
| 室间ANOVA比对 | DataFrame 实验室+结果 | lab_col="实验室", value_col="结果" |
| Z值分析 | 同上 | 同上 |
| Youden 图 | 两个等长数组 | data_a, data_b |
| 批次比对 | DataFrame 批次+结果 | batch_col="批次", value_col="结果" |
| 标准曲线 | 两个等长数组（浓度, 响应） | x, y |
| LOD/LOQ | sigma + slope 或 calibration_data | 见 calc_lod_loq |
| 回收率 | 测定值数组 + 加标浓度 | measured, spiked |
| 曲线不确定度 | calibration_data + 样品响应数组 | calibration_data, sample_responses |
| 趋势监控 | DataFrame 日期+值 | date_col="日期", value_col="值" |
| Prophet 预测 | 同上 | 同上（可选 group_col） |
| 分组分析 | DataFrame 分组列+数值列 | group_col, value_col |
| PCA | 纯数值 DataFrame | 所有列参与分析 |
| 线性回归 | 两个等长数组 | x, y |
| ANOVA | 字典 {组名: [值]} 或列表 [[值]] | groups |
