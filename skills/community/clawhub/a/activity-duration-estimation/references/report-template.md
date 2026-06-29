# HTML评估报告 — 数据接口与生成规范

> 本文件定义 REPORT_DATA 数据结构的完整接口，以及分析结果→格式化→填充→生成的标准化流程。

---

## 一、数据接口：REPORT_DATA

模板使用 `{{REPORT_DATA_JSON}}` 占位符，执行时替换为 JSON 字符串。模板加载后自动解析并渲染。

### 顶层结构

```json
{
  "title": "项目名称",
  "subtitle": "副标题/方法摘要",
  "date": "生成日期",
  "methods": [ ... ],
  "phases": [ ... ],
  "results": { ... },
  "monteCarlo": { ... },
  "multiMcSvg": "SVG字符串",
  "multiMcStats": [ ... ],
  "ganttSvg": "SVG字符串",
  "cpmTable": "HTML表格字符串",
  "overlapSvg": "SVG字符串",
  "overlapStats": [ ... ],
  "analysis": [ ... ]
}
```

### 字段详解

#### methods — 方法列表

```json
[
  {"name": "β分布(PERT)", "desc": "标准三点估算..."},
  {"name": "CPM关键路径", "desc": "基于紧前关系..."}
]
```
- `name`: 方法名称（简短）
- `desc`: 方法说明（一句话）

#### phases — 输入参数

```json
[
  {"name": "前端开发", "o": 5, "m": 10, "p": 20, "alpha": 2.33, "beta": 3.67}
]
```
- `o`/`m`/`p`: 乐观/最可能/悲观
- `alpha`/`beta`: PERT-Beta分布形状参数（必须计算，不可省略）

#### results — 计算结果对比

```json
{
  "直接估算": {"value": 45.0, "unit": "天", "note": "参考基线"},
  "β分布(PERT)": {"value": 47.2, "unit": "天", "note": "推荐"},
  "标准差": {"value": 5.6, "unit": "天", "note": "68%置信区间"}
}
```
- key 为方法名，value 为 `{value, unit, note}` 对象
- `value` 必须为数字类型
- 会渲染为卡片 + 柱状图

#### monteCarlo — PERT-Beta蒙特卡洛（canvas图表）

```json
{
  "stats": {"count": 5000, "min": 36, "max": 62, "mean": 47.8, "stddev": 5.6},
  "p50": 47.2, "p90": 55.3,
  "p50Desc": "50%概率 ... 计划基准",
  "p90Desc": "90%概率 ... 风险缓冲",
  "density": [0.001, 0.005, ...],
  "binLabels": [36.5, 37.5, ...],
  "cumulative": [0.001, 0.006, ...]
}
```
- `density`: 每个区间的频率密度（总数=25）
- `binLabels`: 每个区间中点的工期值（总数=25）
- `cumulative`: 累计概率（递增至1.0，总数=25）
- 这三个数组驱动 canvas 柱状图和折线图

#### multiMcSvg — 多分布对比SVG（由 analysis_engine.generate_mc_svg 生成）

```
SVG 字符串（可直接 innerHTML）
```

#### multiMcStats — 多分布统计卡片

```json
[
  {"label": "PERT-Beta", "value": "47.8±5.6", "note": "P50=47.2 P90=55.3"},
  {"label": "三角分布", "value": "...", "note": "..."}
]
```

#### ganttSvg — 甘特图SVG（由 analysis_engine.generate_gantt_svg 生成）

```
SVG 字符串
```

#### cpmTable — CPM数据表HTML

```html
<table class="data-table">
  <thead><tr><th>任务</th><th>ES</th><th>EF</th><th>LS</th><th>LF</th><th>TF</th><th>关键</th></tr></thead>
  <tbody>
    <tr><td>任务1</td><td>0.0</td><td>10.0</td><td>0.0</td><td>10.0</td><td>0.0</td><td>🔴关键</td></tr>
  </tbody>
</table>
```

#### overlapSvg — 重叠分析SVG

```
SVG 字符串（双面板：最大重叠数 + 最长重叠时长）
```

#### overlapStats — 重叠分析统计

```json
[
  {"label": "最大重叠任务数", "value": "3", "note": "时长120h"},
  {"label": "最长重叠时长", "value": "120h", "note": "重叠3个任务"}
]
```

#### depTable — 紧前关系表

```html
<table class="data-table">
  <thead><tr><th>任务</th><th>前置依赖</th><th>关键</th></tr></thead>
  <tbody>
    <tr><td>任务2</td><td>任务1 (FS)</td><td>🔴</td></tr>
  </tbody>
</table>
```
- 在 CPM/Gantt 章节中，显示在甘特图上方
- 展示每个任务的依赖关系和关系类型（FS/SS/FF/SF）
- 关键列用 🔴 标记该任务是否为关键路径任务

#### analysis — 分析建议

```json
[
  {"type": "positive", "text": "<strong>工程结论：</strong>总工期约47天..."},
  {"type": "warning", "text": "<strong>关键路径风险：</strong>3个任务均为关键..."},
  {"type": "warning", "text": "<strong>任务重叠：</strong>检测到3个任务重叠..."},
  {"type": "warning", "text": "<strong>进度建议：</strong>建议预留应急储备..."},
  {"type": "positive", "text": "<strong>分布对比：</strong>三种分布相互验证..."}
]
```
- `type`: 固定为 `positive`（正面结论）或 `warning`（风险提示）
- `text`: 含 `<strong>` 标签的结构化HTML文本
- **LLM生成时必须覆盖以下5个维度**：
  1. 工程结论（工期+关键路径）
  2. 关键路径风险（TF=0的任务）
  3. 任务重叠影响（资源冲突）
  4. 进度风险缓冲（置信区间）
  5. 多分布对比验证

---

## 二、分析→报告标准化流程

### Step 1: 执行分析计算

使用 `scripts/analysis_engine.py` 中的函数：

| 分析类型 | 函数 | 返回 |
|---------|------|------|
| CPM关键路径 | `calc_cpm(durations, dependencies)` | CPMResult |
| 多分布MC | `monte_carlo_multi(phases, iterations, distributions)` | dict |
| 重叠分析 | `calc_overlap(tasks)` | dict |
| 甘特图SVG | `generate_gantt_svg(tasks, cpm_result)` | SVG string |
| MC对比SVG | `generate_mc_svg(mc_results)` | SVG string |

### Step 2: 格式化数据为 REPORT_DATA 结构

```python
import json
from analysis_engine import *

# 2a. 提取MC直方图数据
h = mc_results['pert']['histogram']
density_list = h['freq']
bin_labels = [(h['edges'][i] + h['edges'][i+1]) / 2
              for i in range(len(h['edges'])-1)]
cumul = []
s = 0
for v in density_list:
    s += v
    cumul.append(round(s, 6))

# 2b. 构建CPM表格HTML
rows = []
for tid in sorted(cpm_result.task_cpm):
    cd = cpm_result.task_cpm[tid]
    crit = '🔴关键' if cd['is_critical'] else ''
    rows.append(f'<tr><td>任务{tid}</td><td>{cd["es"]:.1f}</td><td>...</td></tr>')
cpm_table = '<table class="data-table">...' + ''.join(rows) + '</table>'

# 2c. 构建完整data dict
data = {
    'title': '项目名称',
    'subtitle': '方法摘要',
    'date': str(date.today()),  # 自动取当天日期
    'methods': [...],
    'phases': [...],
    'results': {...},
    'monteCarlo': {
        'stats': {...},
        'p50': ..., 'p90': ...,
        'density': density_list,
        'binLabels': bin_labels,
        'cumulative': cumul,
    },
    'multiMcSvg': mc_svg,
    'multiMcStats': [...],
    'ganttSvg': gantt_svg,
    'cpmTable': cpm_table,
    'overlapSvg': overlap_svg,
    'overlapStats': [...],
    'analysis': [
        # 5维度分析建议
    ],
}
```

### Step 3: 注入模板并输出

```python
with open('scripts/templates/report-template.html', 'r', encoding='utf-8') as f:
    html = f.read()

data_json = json.dumps(data, ensure_ascii=False)
html = html.replace('{{REPORT_DATA_JSON}}', data_json)

with open('estimate_report.html', 'w', encoding='utf-8') as f:
    f.write(html)
```

---

## 三、分析建议生成规范（LLM 执行）

分析建议（`analysis[]`）由 LLM 在 Phase 4 生成，必须遵守以下规范：

### 输出格式

每条建议为 `{"type": "positive"|"warning", "text": "<strong>标题：</strong>分析内容..."}`

| type | 含义 | 示例 |
|------|------|------|
| `positive` | 正面结论、验证通过 | 工程结论、分布验证 |
| `warning` | 风险提示、改进建议 | 关键路径风险、重叠冲突 |

### 必须覆盖的5个维度

| 序号 | 维度 | 数据来源 | 说明 |
|:----:|------|---------|------|
| 1 | **工期+关键路径结论** | CPM.result.critical_path, project_duration | 总工期、关键路径任务列表 |
| 2 | **关键路径风险** | CPM.task_cpm[].is_critical, TF=0 | TF=0的任务列表及影响 |
| 3 | **任务重叠影响** | overlap.max_count, max_duration | 重叠数量、时长、涉及任务 |
| 4 | **进度风险缓冲** | MC.quantiles.p50, p90, stats.stddev | P50/P90、±1σ区间 |
| 5 | **多分布对比** | MC各分布的stats.mean | PERT/三角/泊松的均值差异 |

### 禁止行为

- 不要重复生成相同维度的建议
- 不要在 text 中使用 HTML 以外的格式（仅 `<strong>`）
- 不要在 type 中使用 `positive`/`warning` 以外的值
- 不要生成空洞的内容（如"建议加强管理"）

---

## 四、模板文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 报告模板 | `scripts/templates/report-template.html` | 含 `{{REPORT_DATA_JSON}}` 占位符 |
| 分析引擎 | `scripts/analysis_engine.py` | CPM/MC/重叠分析/SVG生成 |
| 使用方式文档 | 本文 | 数据接口与生成规范 |

---

## 五、快速操作卡

```python
# 完整流程（Phase 4 执行）
from analysis_engine import *
import json

# 1. 分析
cpm = calc_cpm(durations, deps)
mc = monte_carlo_multi(phases, 5000, ['pert','triangular','poisson'])
ol = calc_overlap(tasks)
mc_svg = generate_mc_svg(mc)
gantt_svg = generate_gantt_svg(tasks, cpm)

# 2. 格式化（按上述规格构造 data dict）

# 3. 注入
with open('scripts/templates/report-template.html', 'r', encoding='utf-8') as f:
    html = f.read()
html = html.replace('{{REPORT_DATA_JSON}}', json.dumps(data, ensure_ascii=False))

# 4. 输出
with open('estimate_report.html', 'w', encoding='utf-8') as f:
    f.write(html)
```
