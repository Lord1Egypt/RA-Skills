---
name: 1688-common-html-report-generator
description: 将文本数据报告快速转换为交互式可视化HTML网页。使用 Python 代码驱动预置模板，只需编写数据配置即可自动生成专业数据看板。适用于市场分析报告、运营数据复盘、行业调研报告、销售数据汇总等场景。触发词：生成HTML报告、生成网页报告、转成可视化网页、做成数据看板、数据可视化、生成HTML看板。
---

# 数据报告可视化生成器

通过 Python 代码驱动预置 HTML 模板，将数据报告转换为交互式可视化网页。AI 编写 Python 数据配置脚本（行数随数据量伸缩，简单报告 ~100 行，复杂报告可达 300-500+ 行），脚本自动处理 HTML/CSS/JS 生成。

## 文件结构

```
1688-common-html-report-generator/
├── SKILL.md                 # 本文件（工作流 + 可视化思路）
├── scripts/
│   ├── generate.py          # ReportBuilder 核心脚本
│   └── template.html        # HTML 模板（暗色主题 + ECharts）
└── references/
    └── chart-bindbook.md    # 图表使用手册：每个组件的适用/禁用场景 + API 签名（写代码前必读）
```

## 工作流程

### Step 1: 读取数据源

读取用户提供的文本/数据文件，**逐章逐节**提取：

- 标题、时间、来源等元信息
- **所有**数据表格（含完整行列，不可省略行或列）
- 章节结构和层级关系
- 关键数字
- 洞察/结论/趋势建议等文字段落

### Step 2: 规划报告结构

**在写代码前，先列出章节规划清单**，逐条对照下方可视化思路指南检查。

规划清单必须满足：

1. **完整性**：原文件有 N 章就必须生成 N 个 section，不可合并或省略
2. **数据零丢失**：每张表格都必须出现在报告中（图表或 `r.table()`）；原文的文字洞察/结论用 `r.insight()` 或表格备注呈现
3. **图表多样化**：至少使用 3 种不同图表类型，禁止全篇只用 bar+pie
4. **叙事节奏**：适度使用 `r.insight()` 做章节过渡和收束，避免纯数据堆砌，但也不要每个图表后都加 insight

#### 可视化思路指南（核心，必读）

##### A. 结构组织原则

1. **图表先行，表格兜底**：优先用图表呈现数据。只有维度太多（≥6列）或包含文本字段时才用表格。**禁止一个 section 只有表格没有图表**。
2. **先总后分**：章节开头用一张全景图（`size="lg"`）给整体印象，再用 `grid` 分列展示细节。
3. **grid 高度平衡**：`grid(2)` 左右体量必须相当。禁止一边大图表、另一边 3 行文字。
4. **图表与表格互补**：图表覆盖核心数值维度，表格保留图表无法展示的文本维度（品牌名、关键词等），不要重复展示相同数据。
5. **叙事过渡**：避免"图表→图表→表格→表格"的纯数据堆砌。

##### B. 图表选型规范

每个图表组件有明确的**适用场景**和**禁用场景**，详见 [references/chart-bindbook.md](references/chart-bindbook.md)。选型时必须同时满足适用条件且不触犯禁用条件。

**选型核心原则**：

1. **量级一致**：同一 series / 同一图表中的数值量级差距不超过 10 倍
2. **有对比才用对比型图表**：雷达图至少 2 个对象，热力图至少 2×3 矩阵且无大面积 0 值
3. **连续数值才用连续色阶**：热力图格子必须是可比较的数值，不能是分类/布尔/枚举
4. **信息密度**：有两个维度时用 `dual_y` 而非两张独立图
5. **容器匹配**：`r.chart()` 仅用于 ECharts 图表，`progress_group`/`metric_grid`/`table` 禁止加 `r.chart()`



##### C. 布局约束

- **grid 最多一层，禁止嵌套**。需要并排 3 个饼图就用顶层 `grid(3)`，不要在 `grid(2)` 里再嵌 `grid(3)`。
- 一个格子内需要多个内容时，用**纵向堆叠**，不要横向再分格。

##### D. 表格精简原则

图表化后的表格应裁剪，但不能丢数据：

1. **图表已覆盖的纯数值列**：从表格中去掉
2. **文本字段列**（品牌名、关键词、建议等）：**必须保留**，图表无法表达
3. **表格行数不可裁剪**：原文 11 行就保留 11 行
4. 裁剪后至少保留"名称+2个文本列"。若只剩 1 列，改用 insight 框

##### E. 多平台章节组织原则

**核心思路：先对比，再展开。** 读者看完平台A再看平台B时已经忘了A的数据，所以必须先用跨平台对比图建立全局印象。

推荐结构：

```
1. 跨平台对比（全局视角，必须有）
   → 全景对比图：分组柱状图/热力图/雷达图，把所有平台放一起（size="lg"）
   → metric_grid：各平台最突出的 1 个数字

2. 分平台细节（展开视角）
   → grid(3) 并列饼图（各平台渠道构成）
   → 各平台 dual_y 图（如：月销量柱 + 客单价线，信息密度翻倍）
   → 各平台详细表格（保留文本维度）
```

**禁止**的组织方式：平台A insight → 平台A图表 → 平台A表格 → 平台B insight → 平台B图表 → 平台B表格（串行罗列，无法横向对比）

### Step 3: 读取 API 文档（必须，不可跳过）

**在写任何代码之前**，必须先读取完整图表使用手册：[references/chart-bindbook.md](references/chart-bindbook.md)

读取后重点确认以下易错签名：
- `kpi` 的参数是 `(label, value, unit, change, down)`，**不支持 `color` 参数**
- `chart_heatmap` 的 `data` 格式是 `[x, y, value]` 三元组列表
- `chart_bar` 的 `dual_y=True` 时，series 里需要 `"type": "bar"/"line"` 和 `"yAxisIndex": 1`
- `chart_pie` 的 `inner_radius`/`outer_radius` 参数可选
- `progress_bar` 的参数顺序是 `(label, value, max_val, color, suffix)`
- `metric` 的参数是 `(value, desc, color)`，`unit` 可选

**禁止跳过此步骤直接写代码**——本文件的 API 速查是精简版，缺少参数细节，仅靠速查表写代码会导致调用出错。

### Step 4: 编写 Python 构建脚本

在当前工作区的 `outputs/` 目录下创建构建脚本，文件名格式为 `build_报告主题_时间戳.py`（如 `outputs/build_市场分析_20260515.py`）。脚本行数不设上限，以**完整还原数据**为第一优先级。

```python
import sys, os
sys.path.insert(0, "1688-common-html-report-generator/scripts")
from generate import ReportBuilder

r = ReportBuilder("报告标题")
r.header("大标题", "副标题", ["时间:2026-05-14", "来源:XX"])
r.nav([("核心指标", "#kpi"), ("平台对比", "#platform")])

with r.section("kpi", "01", "核心指标", "关键数据概览"):
    r.kpi_grid()
    r.kpi("销量", "4.23", "亿件", "同比+14.9%")
    r.kpi("均价", "89", "元", "同比-5.2%", down=True)
    r.kpi_end()

    # grid(2) 示例：左右体量对等
    r.grid(2)
    r.card("销量对比", dot_color=r.C_TAOBAO)
    r.chart("barChart")
    r.chart_bar("barChart",
        categories=["抖音", "淘宝", "小红书"],
        series=[{"name": "销量", "data": [120, 200, 80], "color": r.C_TAOBAO}],
        show_label=True)
    r.card_end()
    r.card("占比分布", dot_color=r.C_DOUYIN)
    r.chart("pieChart")
    r.chart_pie("pieChart", data=[
        {"value": 45, "name": "抖音", "color": r.C_DOUYIN},
        {"value": 35, "name": "淘宝", "color": r.C_TAOBAO},
        {"value": 20, "name": "小红书", "color": r.C_XIAOHONGSHU},
    ])
    r.card_end()
    r.grid_end()

    r.insight("核心发现", ["要点1", "要点2"])

r.footer("数据来源：XX平台")
os.makedirs("outputs", exist_ok=True)
r.render("outputs/报告.html")
```

### Step 5: 执行并交付

```bash
python3 build_报告主题_时间戳.py
open outputs/报告.html
```

## 关键约束

- **不要手写 HTML/CSS/JS**，全部通过 `ReportBuilder` 方法生成
- **不要手写 ECharts 通用配置**（tooltip/legend/grid 已内置），不满足时用 `chart_script`
- **颜色引用常量**（`r.C_DOUYIN` 等），保持跨图表一致
- **脚本行数不设上限**：数据量大时可 300-500+ 行，以完整还原为第一目标
