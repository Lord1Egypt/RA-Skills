# Data Format Reference

> **何时读我**：拿到报错 KeyError/字段缺失，或不确定某图型 JSON 怎么写。
> **最短路径**：Ctrl-F 图型名 → 照 schema 抄字段。
> **回 INDEX**：SKILL.md「文件索引与 30 秒路由」。

Input: JSON (`.json`) or CSV (`.csv`/`.tsv`). All values are floats unless noted.

## Bar Chart (`--type bar`)

```json
{
  "labels": ["Group A", "Group B", "Group C"],
  "series": {
    "Series 1": [10.5, 20.3, 15.2],
    "Series 2": [12.0, 18.7, 16.5]
  },
  "errors": {
    "Series 1": [1.2, 0.8, 1.5],
    "Series 2": [0.9, 1.1, 0.7]
  },
  "significance": {
    "Series 1:0": "***",
    "Series 1:1": "*",
    "Series 1:2": "NS"
  }
}
```

- `labels` (array): X-axis group labels
- `series` (object): Each key = series name, value = array of bar heights
- `errors` (object, optional): Per-bar error values. Key must match series name
- `significance` (object, optional): `"series_prefix:group_index"` → label (`*`, `**`, `***`, `NS`)

### CSV equivalent
```
Group,Series1,Series2
A,10.5,12.0
B,20.3,18.7
C,15.2,16.5
```

### 组间显著性括号（`comparisons`，v6.9+，`--sig-bracket`）

bar/grouped_bar/box/violin 可携带比较对，`--sig-bracket` 开启后自动画分层 bracket+星号（<0.05 `*`、<0.01 `**`、<0.001 `***`，p≥0.05 显示 `NS`）：

```json
{
  "labels": ["ctrl", "trt1", "trt2"],
  "series": {"weight": [5.03, 4.66, 5.53]},
  "comparisons": [
    {"a": "ctrl", "b": "trt2", "p": 0.049},
    {"a": "trt1", "b": "trt2", "p": 0.0031}
  ]
}
```

`a`/`b` 必须是组名（labels/分组名）；p 值来自你自己的统计分析
（引擎只做可视化，不替你选检验）；bracket 按区间自动分层防重叠。

Note: since v6.0, CSV supports error bars via suffix columns (`X_se` / `X_sd` / `X_sem` / `X_err` auto-paired with the main column; `X_sd` + `X_n` → SEM). Significance marks remain JSON-only.

---

## Heatmap (`--type heatmap`)

```json
{
  "matrix": [[10, -5, 3], [8, 12, -2], [-1, 7, 15]],
  "row_labels": ["Row A", "Row B", "Row C"],
  "col_labels": ["Col 1", "Col 2", "Col 3"],
  "cbar_label": "Value (units)"
}
```

- `matrix` (2D array): Values for heatmap cells
- `row_labels` / `col_labels`: Axis labels
- `cbar_label` (optional): Colorbar label
- Override range: `--vmin -20 --vmax 45 --cmap RdBu_r`

---

## Scatter Plot (`--type scatter`)

```json
{
  "x": [1.2, 2.3, 3.1, 4.5],
  "y": [5.1, 6.2, 4.8, 7.3],
  "groups": ["A", "A", "B", "B"]
}
```

- `x`, `y`: Data arrays (equal length)
- `groups` (optional): Color grouping. Values become legend entries

---

## Line Chart (`--type line`)

```json
{
  "labels": ["Jan", "Feb", "Mar"],
  "series": {
    "Revenue": [42, 48, 55],
    "Profit": [12, 15, 18]
  },
  "errors": {
    "Revenue": [3, 2, 4],
    "Profit": [1, 1.5, 2]
  }
}
```

- `labels`: X-axis labels
- `series`: Named line series
- `errors` (optional): Error band width per series

### CSV equivalent
```
Month,Revenue,Profit
Jan,42,12
Feb,48,15
Mar,55,18
```

---

## Box Plot (`--type box`)

```json
{
  "labels": ["Treatment A", "Treatment B", "Control"],
  "series": {
    "Treatment A": [10, 12, 11, 13, 10, 14],
    "Treatment B": [8, 9, 10, 7, 11, 9],
    "Control": [5, 6, 4, 7, 5, 6]
  }
}
```

Each series value is an array of raw data points.

---

## Forest Plot (`--type forest`)

### Basic (v1.0)

```json
{
  "labels": ["Study A", "Study B", "Study C"],
  "estimates": [1.2, 0.8, 1.5],
  "ci_low": [0.9, 0.5, 1.1],
  "ci_high": [1.6, 1.3, 2.0],
  "overall": {
    "estimate": 1.1,
    "ci_low": 0.85,
    "ci_high": 1.35
  },
  "ref_line": 1.0
}
```

- `labels`: Study names (Y-axis)
- `estimates`: Point estimates
- `ci_low` / `ci_high`: Confidence interval bounds
- `overall` (optional): Diamond summary estimate
- `ref_line` (optional): Reference/null line. Default: auto by `measure` (OR/RR/HR → 1.0, MD/SMD → 0.0; log-scale data pass `ref_line`: 0 explicitly)

### Enhanced (v1.3.0) — Recommended for meta-analysis

```json
{
  "labels": ["Smith 2020", "Jones 2021", "Wang 2022"],
  "estimates": [1.35, 0.89, 1.52],
  "ci_low": [0.95, 0.65, 1.10],
  "ci_high": [1.92, 1.22, 2.10],
  "weights": [25.3, 18.7, 22.1],
  "events": [
    {"events": 45, "total": 120},
    {"events": 32, "total": 95},
    {"events": 58, "total": 150}
  ],
  "overall": {
    "estimate": 1.28,
    "ci_low": 1.05,
    "ci_high": 1.56
  },
  "ref_line": 1.0,
  "measure": "OR (95% CI)",
  "heterogeneity": {
    "Q": 8.32,
    "df": 4,
    "I2": 51.9,
    "p": 0.081
  }
}
```

- `weights` (optional): Study weights → bubble size (larger weight = larger bubble)
- `events` (optional): Array of `{"events": int, "total": int}` per study → displayed as "Events/Total" column
- `measure` (optional): Effect measure label ("OR", "RR", "HR", "MD", "SMD") → displayed on x-axis
- `heterogeneity` (optional): Object with `Q`, `df`, `I2`, `p` → displayed as footer annotation
  - `I2`: I² statistic (percentage)
  - `Q`: Cochran's Q statistic
  - `df`: degrees of freedom
  - `p`: p-value for heterogeneity test

---

## Violin Plot (`--type violin`)

Same data format as Box Plot — each series is an array of raw data points.

```json
{
  "labels": ["Treatment", "Control", "Placebo"],
  "series": {
    "Treatment": [8, 9, 10, 7, 11, 9, 8, 12],
    "Control": [5, 6, 4, 7, 5, 6, 4, 5],
    "Placebo": [6, 5, 7, 5, 6, 4, 6, 5]
  }
}
```

---

## Kaplan-Meier Survival Curve (`--type km` or `--type survival`)

### Format 1: Raw time-to-event data (recommended)

```json
{
  "groups": {
    "Treatment": [[12, 1], [24, 1], [36, 0], [48, 1], [60, 0]],
    "Control": [[6, 1], [10, 1], [18, 1], [30, 1], [42, 0]]
  },
  "log_rank": {"p": 0.032, "method": "Log-rank"},
  "median_survival": {"Treatment": 36.5, "Control": 14.2},
  "risk_table": {
    "times": [0, 12, 24, 36, 48],
    "Treatment": [50, 42, 35, 28, 20],
    "Control": [50, 38, 25, 15, 8]
  }
}
```

- `groups`: Object with group names as keys. Each value is an array of `[time, event]` pairs where `event` = 1 (event/death) or 0 (censored). For all-events data (no censoring), use a flat array: `[[12], [24], ...]` or `[12, 24, ...]`.
- `log_rank` (optional): Object with `p` (p-value) and `method` (test name). Displayed as annotation box.
- `median_survival` (optional): Object mapping group names to median survival times. Draws vertical dotted lines.
- `risk_table` (optional): Object with `times` array and per-group at-risk counts.

### Format 2: Pre-computed survival probabilities

```json
{
  "time": [0, 3, 6, 9, 12, 18, 24, 36],
  "survival": {
    "Treatment": [1.0, 0.95, 0.88, 0.82, 0.75, 0.68, 0.60, 0.52],
    "Control": [1.0, 0.88, 0.72, 0.58, 0.45, 0.32, 0.22, 0.15]
  },
  "censored": {
    "Treatment": [0, 0, 1, 0, 0, 1, 0, 0],
    "Control": [0, 0, 0, 1, 0, 0, 0, 0]
  },
  "log_rank": {"p": 0.008}
}
```

- `time`: Shared time axis array.
- `survival`: Per-group survival probability arrays.
- `censored` (optional): Per-group censoring indicators (1 = censored at that time point).

---

## Competing-Risk Cumulative Incidence (`--type cif`, v5.7)

### Long-format subjects (required)

```json
{
  "time": [3, 5, 6, 7, 8, 10, 12, 12],
  "event": [1, 2, 1, 0, 1, 2, 0, 1],
  "cause_labels": {"1": "复发", "2": "移植相关死亡"},
  "time_unit": "月",
  "compare_km": "auto"
}
```

- `time`: 等长数组，随访时长 ≥0（与 `event` 一一对应）。
- `event`: 整数编码 —— `0`=删失，`1`=目标事件，`≥2`=竞争事件编号（2、3… 各画一条）。
- `cause_labels` (optional): `{"编码": "名称"}`，图例命名各原因；缺省「目标事件/竞争事件 N」。
- `time_unit` (optional): x 轴单位（如「月」）。
- `compare_km` (optional): `auto`（默认，有竞争事件才画）/`true`/`false` —— 叠加 1−KM 朴素对照虚线（竞争事件当删失，系统性高估目标事件风险）。
- `percent` (optional): `true` 时 y 轴 0–100%。
- `y_max` (optional): y 轴上限（轴单位数值）。
- 边界：单队列按事件原因分层（多臂分组用 `-t km`，events 含 ≥2 自动切 AJ 模式）；stderr 报告事件计数、末点各因 CIF 与 1−KM 高估幅度（百分点）。
- 真实数据示例：`examples/realworld/hematology_mgus_cif.json`（Mayo Clinic mgus2 队列）。

---

## ROC Curve (`--type roc`)

### Single curve

```json
{
  "fpr": [0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.50, 1.0],
  "tpr": [0.0, 0.45, 0.68, 0.82, 0.88, 0.92, 0.96, 1.0],
  "auc": 0.912,
  "ci": {"low": 0.854, "high": 0.958},
  "cutoff": {"fpr": 0.15, "tpr": 0.88, "threshold": 2.35}
}
```

- `fpr` / `tpr`: False positive rate and true positive rate arrays.
- `auc` (optional): AUC value. Auto-computed via trapezoidal rule if omitted.
- `ci` (optional): 95% confidence interval `{"low": float, "high": float}`.
- `cutoff` (optional): Optimal cutoff point with `fpr`, `tpr`, and optional `threshold`.
- `diagonal` (optional, default true): Show diagonal reference line.

### Multiple curves (model comparison)

```json
{
  "curves": [
    {
      "name": "CRP + ESR",
      "fpr": [0.0, 0.05, 0.12, 0.25, 0.50, 1.0],
      "tpr": [0.0, 0.55, 0.78, 0.88, 0.95, 1.0],
      "auc": 0.897
    },
    {
      "name": "IL-6 + CRP",
      "fpr": [0.0, 0.03, 0.08, 0.18, 0.45, 1.0],
      "tpr": [0.0, 0.62, 0.85, 0.92, 0.97, 1.0],
      "auc": 0.942
    }
  ]
}
```

- `curves`: Array of curve objects, each with `name`, `fpr`, `tpr`, and optional `auc`.

---

## Stacked Bar Chart (`--type stacked_bar`)

```json
{
  "labels": ["GPA", "MPA", "EGPA"],
  "series": {
    "Renal": [35, 15, 5],
    "Pulmonary": [25, 30, 45],
    "ENT": [20, 5, 30],
    "Neurologic": [10, 25, 10],
    "Skin": [10, 25, 10]
  },
  "percentage": false,
  "show_total": true
}
```

- `labels`: X-axis group labels.
- `series`: Each key = subgroup name, value = array of values per group.
- `percentage` (optional, default false): If true, display percentage labels instead of raw values.
- `show_total` (optional, default false): If true, show total N on top of each bar.

### CSV equivalent
```
Group,Renal,Pulmonary,ENT,Neurologic,Skin
GPA,35,25,20,10,10
MPA,15,30,5,25,25
EGPA,5,45,30,10,10
```

---

## Volcano Plot (`--type volcano`, v4.4)

```json
{
  "log2fc": [2.1, -1.3, 0.1],
  "pvalue": [1e-6, 0.03, 0.7],
  "names": ["GeneA", "GeneB", "GeneC"],
  "fc_cut": 1.0,
  "p_cut": 0.05,
  "top": 10
}
```

- `log2fc` / `pvalue`: 两个**等长**数值数组；p ∈ (0, 1]（p=0 请用最小可表示值如 1e-300）。
- `names`（可选）：与 log2fc 等长的名称数组；显著性 Top-N 自动标注。
- `fc_cut`（默认 1.0）/ `p_cut`（默认 0.05）/ `top`（默认 10）：阈值与标注数量。
- 形态：x=log2FC，y=-log10(p)；上调暖橙/下调蓝/非显著灰；阈值虚线 + 计数事实框。
- 组学差异表达（基因/蛋白/代谢物）；多组比较请改用 line/bar 系列。

---

## UpSet Plot (`--type upset`, v4.7)

```json
{
  "title": "五组学平台差异基因交集",
  "sets": {
    "转录组": ["TP53", "KRAS", "EGFR", "BRCA1"],
    "蛋白组": ["TP53", "EGFR", "MYC", "BRCA1"],
    "甲基化": ["TP53", "BRCA1", "CDKN2A"],
    "eQTL": ["KRAS", "EGFR", "PTEN"],
    "GWAS": ["TP53", "BRCA1", "ERBB2"]
  },
  "top_n": 12,
  "min_size": 1,
  "sort": "size"
}
```

- `sets`：**≥2 个**集合（推荐 ≥5；2~4 集合用 venn 更直观），值为元素列表，自动求交集并集；
  元素为字符串/数值标量，集合数上限 30。
- `top_n`（默认 12，取 1~50）：按排序展示前 N 个交集；未展示交集只计入 stderr 事实行。
- `min_size`（默认 1）：过滤元素数小于该值的交集。
- `sort`：`size`（默认，交集大小降序）或 `degree`（交集度数优先）；同数据同图（确定性三键 tie-break）。
- 形态：顶部=交集大小柱（计数直标）；中部=点阵（行=集合、列=交集，实心点+竖连线）；
  左下=集合总大小横条。标题放 JSON `title` 字段（CLI `--title` 对自管图型不生效）。

---

## Raincloud Plot (`--type raincloud`, v4.9)

```json
{
  "labels": ["活动期", "低活动期", "健康对照"],
  "datasets": {
    "活动期": [12.1, 14.2, 15.8, 13.4, 16.1],
    "低活动期": [6.2, 7.1, 5.8, 6.9],
    "健康对照": [3.1, 2.8, 3.5, 3.0]
  },
  "jitter": 0.08,
  "cloud_scale": 1.0
}
```

- 分布三合一（Allen et al. 2021 现代形态）：左=KDE 半小提琴「云」（密度形状）+中=箱线「五数概括」
  （IQR 箱+中位粗线+1.5×IQR 须）+右=抖动原始点「雨」（确定性抖动，同数据同图）。
- schema 与 violin 完全相同（labels 可省略，省略时用 datasets 键名）。
- `jitter`（默认 0.08，取 0~0.3）：雨滴横向散布幅度；`cloud_scale`（默认 1.0，取 0~2.0）：云的宽度缩放，0=隐藏云（仅箱+雨，stderr 告知）。
- `--stats auto/multi/bootstrap` 与 box/violin 同样适用（显著性括号自动标注）。
- 方差为 0 的组（全同值）KDE 退化 → 云自动退化为标记线并在 stderr 告知（零静默）。

---

## Waterfall Plot (`--type waterfall`, v4.8)

```json
{
  "change": [-45.2, -62.0, -28.7, 12.6, 41.7],
  "names": ["P001", "P002", "P003", "P004", "P005"],
  "group": ["PR", "PR", "SD", "PD", "PD"],
  "pr_cut": -30.0,
  "pd_cut": 20.0,
  "sort": "desc"
}
```

- `change`：必填，每例（患者/样本）自基线最佳变化百分比（肿瘤缩小为负、增大为正）。
- `names`（可选）：x 轴标识（如患者编号）；缺省 P01…Pnn。
- `group`（可选）：缓解类别（如 RECIST CR/PR/SD/PD）——按类别着色+图例+计数事实框；
  全为 CR/PR/SD/PD（大小写不敏感，图例与计数归一为大写规范形）时用规范语义色，其余类别用主题色。
  未给 group 时按阈值分桶着色（≤pr_cut 缓解蓝/中间稳定灰/≥pd_cut 进展橙）。
- `pr_cut`（默认 -30）/ `pd_cut`（默认 20）：阈值虚线（须 pr_cut<0<pd_cut）。
- `sort`：`desc`（默认，变化降序=经典瀑布形态，并列按输入序）或 `input`（保持给定顺序）。
- `--show-values`：柱端数值标注；`y_label` 自定义 y 轴标题。

---

## Slope Chart (`--type slope`, v4.2)

```json
{
  "left_label": "基线",
  "right_label": "12 周",
  "items": {
    "药物A": [72, 85],
    "药物B": [65, 61],
    "对照": [70, 71]
  }
}
```

- `items`: **恰好 2 个数值** `[左值, 右值]` 每项；至少 2 项。
- `left_label` / `right_label`（可选）：两端列标题（默认 Before/After）。
- 形态：每项一条左→右连线，两端直标"名称+数值"（自动避让）；
  最大上升项主题色强调、最大下降项暖橙。多时点请改用 line。

---

## Dual Y-Axis Chart (`--type dual_axis`) — left bars + right lines

```json
{
  "labels": ["Baseline", "Wk 4", "Wk 8", "Wk 12", "Wk 24"],
  "left": {
    "CRP (mg/L)": [45, 32, 18, 12, 8]
  },
  "right": {
    "DAS28": [5.6, 4.8, 3.9, 3.2, 2.6]
  },
  "left_errors": {
    "CRP (mg/L)": [5, 4, 3, 2, 1]
  },
  "right_errors": {
    "DAS28": [0.4, 0.3, 0.3, 0.2, 0.2]
  },
  "left_ylabel": "CRP (mg/L)",
  "right_ylabel": "DAS28"
}
```

- `labels`: X-axis labels (time points).
- `left` / `y1`: Series for the **left Y-axis** — drawn as grouped BARS by default (v3.10).
- `right` / `y2`: Series for the **right Y-axis** — drawn as dashed LINES by default (v3.10).
- `left_type` (optional, v3.10): `"bar"` (default) or `"line"` — form of the left-axis series.
- `right_type` (optional, v3.10): `"line"` (default) or `"bar"` — form of the right-axis series.
- `left_floor` / `right_floor` (optional, v3.10): numeric lower bound for that Y-axis —
  e.g. `"right_floor": 35` starts a percentage axis at a clean 35 (journal convention);
  default keeps matplotlib's 5% margin. Ignored (with a warning) if ≥ the data maximum.
- Legend: merged from both axes, drawn frameless in a reserved top band (never occludes data);
  CLI `--legend-loc` / `--legend-outside` override.
- `left_errors` / `y1_errors` (optional): Error band values for left axis series.
- `right_errors` / `y2_errors` (optional): Error band values for right axis series.
- `left_ylabel` (optional): Left Y-axis label.
- `right_ylabel` (optional): Right Y-axis label.

Multiple series per axis are supported:
```json
{
  "labels": ["Jan", "Feb", "Mar"],
  "left": {"CRP": [45, 32, 18], "ESR": [60, 42, 28]},
  "right": {"DAS28": [5.6, 4.8, 3.9]}
}
```

---

## Horizontal Bar Chart (`--type hbar` or `--type bar --horizontal`)

Same data format as Bar Chart. The only difference is orientation — use hbar when group labels are long or when comparing many groups (avoids label crowding).

```json
{
  "labels": ["Infliximab", "Adalimumab", "Tocilizumab", "Rituximab", "Abatacept"],
  "series": {
    "ACR50": [45, 52, 58, 48, 42],
    "ACR70": [28, 32, 38, 30, 25]
  },
  "errors": {
    "ACR50": [4, 5, 4, 3, 4],
    "ACR70": [3, 4, 3, 3, 3]
  }
}
```

CLI flags: `--horizontal` or use `-t hbar`. Combine with `--show-ratio` to display fold-change annotations.

---

## Multi-Panel Composite (`--type composite`)

Layout multiple chart panels (A, B, C...) in a single figure. Each panel can be any chart type. This is the standard journal figure layout (e.g., Figure 1A = bar, 1B = line, 1C = scatter).

```json
{
  "layout": [1, 3],
  "panels": [
    {
      "title": "Panel A: ACR50 Response",
      "type": "bar",
      "pos": [0, 0],
      "data": {
        "labels": ["Wk12", "Wk24", "Wk52"],
        "series": {"Treatment": [62, 71, 78], "Control": [28, 32, 35]}
      },
      "ylabel": "ACR50 (%)",
      "show_values": true,
      "legend": false
    },
    {
      "title": "Panel B: CRP Dynamics",
      "type": "line",
      "pos": [0, 1],
      "data": {
        "labels": ["Baseline", "Wk4", "Wk12", "Wk24", "Wk52"],
        "series": {"Treatment": [28, 12, 6, 4, 3], "Control": [27, 24, 22, 20, 19]}
      },
      "ylabel": "CRP (mg/L)",
      "xlabel": "Time"
    },
    {
      "title": "Panel C: Remission Rate",
      "type": "scatter",
      "pos": [0, 2],
      "data": {
        "x": [1, 2, 3, 4, 5, 6],
        "y": [15, 22, 31, 38, 45, 52],
        "groups": ["Treat", "Treat", "Treat", "Ctrl", "Ctrl", "Ctrl"]
      },
      "ylabel": "Remission (%)",
      "trend": false
    }
  ]
}
```

- `layout` (array): `[rows, cols]` grid layout
- `panels` (array of objects): Each panel has:
  - `title`: Panel title
  - `type`: Any chart type from the generator (`bar`, `line`, `scatter`, `heatmap`, etc.)
  - `pos`: `[row, col]` position in the grid (0-indexed)
  - `data`: Data object matching the panel's chart type (see other sections for schema)
  - `xlabel`, `ylabel` (optional): Per-panel axis labels
  - `show_values`, `legend`, `trend`, `hatch`, `horizontal`, `show_ratio` (optional): Per-panel flags
- `share_y` (bool, optional, v5.6): when true, panels sharing the same `ylabel`
  (same-variable semantics) are unified to one y scale (log scales sync too);
  the unified range is reported on stderr. Use when reviewers would misread
  panels whose identical-variable axes span very different ranges — `--doctor`
  flags that case (>5× spread) and points here.

---

## Architecture/Flow Diagram (`--type diagram`)

Draw colored blocks connected by arrows, with optional group boxes and annotations. Useful for study design diagrams, CONSORT flow charts, and conceptual architecture.

```json
{
  "background": "light",
  "blocks": [
    {"id": "A", "label": "Patient Data", "x": 0, "y": 1, "w": 2.5, "h": 1.2, "color": "#0072B2"},
    {"id": "B", "label": "Screen", "sublabel": "ACR/EULAR Criteria", "x": 3.5, "y": 1, "w": 2.5, "h": 1.2, "color": "#009E73", "shape": "round"},
    {"id": "C", "label": "Treatment", "x": 7, "y": 2.5, "w": 2.5, "h": 1.2, "color": "#D55E00"}
  ],
  "arrows": [
    {"from": "A", "to": "B", "label": "n=240"},
    {"from": "B", "to": "C", "style": "->", "rad": 0.1}
  ],
  "groups": [
    {"blocks": ["B", "C"], "label": "Intervention Phase", "color": "#56B4E9", "style": "dashed"}
  ],
  "annotations": [
    {"text": "Study Design", "x": 5, "y": 4.5, "fontsize": 12, "color": "#E69F00", "weight": "bold"}
  ]
}
```

- `background` (optional): always `"light"` — dark backgrounds are NEVER allowed (publication standard)
- `blocks` (array): Each block object has:
  - `id`: Unique identifier (used in arrows)
  - `label`: Main text label
  - `sublabel` (optional): Smaller secondary text
  - `x`, `y`: Bottom-left position (arbitrary coordinate space)
  - `w`, `h`: Width and height
  - `color` (optional): Fill color hex (defaults to theme palette)
  - `shape` (optional): `"round"` (default, rounded corners) or `"rect"` (sharp corners)
- `arrows` (array): Each arrow object has:
  - `from`, `to`: Block IDs to connect
  - `label` (optional): Text on the arrow
  - `style` (optional): Arrow style (default `"->"`)
  - `rad` (optional): Curve radius for curved arrows (default `0` = straight)
  - `color` (optional): Arrow color
- `groups` (array): Dashed bounding boxes around sets of blocks:
  - `blocks`: Array of block IDs to enclose
  - `label`, `color`, `style` (optional): Group box styling
- `annotations` (array): Free-text labels at arbitrary positions:
  - `text`, `x`, `y`: Content and position
  - `fontsize`, `color`, `weight`, `ha`, `va` (optional): Styling


## PRISMA 流程图（`-t prisma`，v2.1.0 新增）

PRISMA 2020 系统综述流程图。必需字段：`records_identified`、`studies_included`。

```json
{
  "records_identified": 128,
  "duplicates_removed": 23,
  "records_screened": 105,
  "records_excluded": 61,
  "reports_sought": 44,
  "reports_not_retrieved": 3,
  "reports_assessed": 41,
  "exclusion_reasons": {"Wrong population": 5, "Wrong intervention": 7, "No usable data": 4},
  "studies_included": 25,
  "lang": "en"
}
```

规则：
- 中间字段可省略，自动按流水线推导（screened = identified − duplicates，sought = screened −
  excluded，assessed = sought − not_retrieved）。
- **自洽性闸门**：显式给出的数字必须与推导一致，`exclusion_reasons` 合计 + `studies_included`
  必须等于 `reports_assessed`，否则 ERROR（exit 1）拒绝出图。
- `lang: "zh"` 输出中文标准措辞（识别/筛选/纳入）；`exclusion_reasons` 的键始终按你给的内容
  原样渲染（中英文均可）。
- 数值为 0 且未显式给出的侧盒自动省略。

## JSON vs CSV 能力对照（v3.1 收拢）

| 能力 | JSON | CSV/TSV |
|---|---|---|
| 基础绘图（柱/线/散点/箱/小提琴等） | ✅ | ✅ |
| 误差棒 | ✅ `errors` 对象 | ✅ 后缀列 `X_se`/`X_sd`/`X_err`（v6.0 起，`--csv-no-errors` 可关） |
| 显著性标记 | ✅ `significance` | ❌ 请改用 JSON |
| KM 风险表/log-rank | ✅ 原始 [时间,事件] 格式 | ❌ |
| 多因素 Cox 森林图 | ✅ 逐例试者数据 | ✅ 长表 CSV 亦可 |
| 组合图 panels / 复杂布局 | ✅ | ❌ |
| Excel 直读 | — | `--sheet` 需 `.xlsx` |

> 原则：需要显著性标记、统计标注或复杂结构时用 JSON；简单数值与误差棒（后缀列）用 CSV 即可。

## ridgeline（v5.0）

schema 同 violin：`labels`（组名，自上而下）+ `datasets`（{组名: [数值...]}）。
可选 `overlap`（0~0.95，山脊纵向重叠比例，默认 0.55）、`sort`（"input"|"median"）、
`x_label`。单值组（仅 1 个不同值）退化为基线标记线并 stderr 告知。

## dumbbell（v5.1）

`{"labels": [...], "from": [...], "to": [...]}`：labels 条目名（可选），
from/to 等长数值数组必填。可选 `from_label`/`to_label`（图例名）、
`sort`（"gap"|"input"|"to"，默认 gap 降序）、`show_values`（点端数值）、
`show_gap`（连接线中点 Δ 标注）、`x_label`。严格两时点：每行仅 from/to 两值。

## calibration（v5.2）

两种等价给法：
1. `bins`: `[{"predicted": 0.1, "observed": 0.13, "n": 30, "ci_lo": 0.04,
   "ci_hi": 0.28}, ...]`（对象数组，n/ci 可选）；
2. `predicted`/`observed` 平行数组 + 可选平行 `ci_lo`/`ci_hi`/`n`。
全值 ∈[0,1]；`hl_p`（0~1）左上角标注 Hosmer-Lemeshow p；`smooth: true` 画
各箱线性插值细线（≥4 箱才有意义）。坐标轴固定等比 0~1（含 4% 端点 pad）。

## dca（v5.2）

`{"thresholds": [...], "models": [{"name": "...", "net_benefit": [...]}, ...]}`：
thresholds 严格升序且在 (0,1) 开区间；models 1~6 个，net_benefit 长度=阈值数。
参照策略二选一或都不给：`prevalence`（0~1，画理论全部干预线）或 `treat_all`
（与 thresholds 等长的实测数组，优先）；`show_none: false` 关闭不干预 0 线。
净收益单位=每 100 人净真阳性（Vickers 定义）。


## nomogram（v5.3）

`{"variables": [{...}], "outcome_scales": [{...}], "total_points_max": 350}`：
variables 1~12 个，每项 `name`+`ticks`（2~12 个）必填，`labels` 自定刻度文字、
`points_at`（0~100，缺省线性均布）可选；outcome_scales 1~3 个，每项
`label`+`ticks`+`points_at`（**总积分口径**，非 0~100）。total_points_max 缺省
=结局尺最大 points_at。引擎只可视化不拟合：points 请来自已拟合模型
（R rms::nomogram / Python 统计包输出），方法学口径写入统计方法段。

## rcs（v5.4）

`{"points": [{"value": 40, "est": 1.02, "ci_lo": 0.72, "ci_hi": 1.45}, ...]}`：
≥5 个网格点（value 单调、来自你拟合的样条模型，引擎不拟合）。可选 `ref`
（参照竖线，惯例=中位数）、`log_y`（默认 true=HR/OR 对数轴；false 时参照
水平线默认 y=0，可用 `hline_at` 覆盖）、`hist`（默认 true，底部暴露 rug）、
`x_label`/`y_label`。解读：曲线偏离参照水平=非线性关联；置信带与参照水平
相交=无统计学差异区。

## subgroup（v5.5）

`{"subgroups": [{"name": "年龄", "p_interaction": 0.48, "levels": [
{"name": "<65", "est": 0.72, "ci_low": 0.55, "ci_high": 0.94, "n": 120, "p": 0.015}, ...]}, ...]}`：
subgroups 1~12 个、levels 每组 2~8 层；`overall`（底部菱形）与 `est_label`
（HR/OR/RR 无效线=1，MD/SMD=0）、`log_x`（默认比率尺度 true）可选。
引擎只可视化不拟合：est/p/交互检验来自你的亚组模型（交互须含交互项的多因素模型）。
