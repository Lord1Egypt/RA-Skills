# Data Format Reference

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

Note: CSV mode does not support errors or significance — use JSON for those.

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
- `ref_line` (optional): Reference/null line (default: 0)

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

## Dual Y-Axis Line Chart (`--type dual_axis`)

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
- `left` / `y1`: Series for the **left Y-axis** (solid lines).
- `right` / `y2`: Series for the **right Y-axis** (dashed lines).
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
