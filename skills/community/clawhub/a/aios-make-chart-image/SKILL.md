---
name: aios-make-chart-image
description: 当 OpenClaw 或 AIOS agent 需要把 JSON、Markdown 表格或 ECharts option 渲染成图表图片时，必须使用本技能。使用内置 JavaScript 脚本解析数据、生成 ECharts 配置，并导出 PNG、SVG、JPEG 或 WebP 图片；不要临时手写浏览器截图流程。
---

# AIOS 图表图片生成

本技能用于把结构化数据生成 ECharts 图表，并导出为图片文件。优先使用内置脚本 `scripts/make_chart_image.mjs`，不要在对话中临时拼一个替代渲染脚本。

## 适用场景

- 用户提供 JSON 数据并要求生成柱状图、折线图、饼图、散点图等图片。
- 用户提供 Markdown 表格并要求生成图表图片。
- 用户提供完整 ECharts option，需要稳定导出为图片。
- 需要把图表文件继续通过 `aios-transfer-file` 返回给用户。

## 不可违反的规则

- 必须在本 skill 目录中运行内置脚本，确保依赖从本地 `node_modules` 解析。
- 本项目统一使用 JavaScript/TypeScript；不要为本技能添加 Python 渲染流程。
- 输出到当前工作区内的 `chart_output` 目录。
- 如果需要把生成的图片发给用户，先生成本地文件，再使用 `aios-transfer-file` 上传返回。
- 如果输入是完整 ECharts option，保留用户提供的 option，只补必要的画布尺寸和背景色。
- 如果输入是表格数据，先选择合适的 `chartType`、分类字段和数值字段；字段不明确时说明假设。

## 依赖处理

本技能在 `package.json` 中声明：

- `echarts`
- `sharp`

首次使用前检查依赖：

```bash
cd /path/to/aios-make-chart-image
npm ls echarts sharp --depth=0
```

如果依赖缺失，在本 skill 目录执行：

```bash
npm install
```

## 基本用法

从 JSON 或 Markdown 文件生成 PNG：

```bash
node scripts/make_chart_image.mjs --input "/abs/path/data.json" --output "/abs/path/chart.png"
node scripts/make_chart_image.mjs --input "/abs/path/table.md" --output "/abs/path/chart.png" --chart-type line
```

从 stdin 读取：

```bash
cat table.md | node scripts/make_chart_image.mjs --input - --output "/abs/path/chart.png"
```

保存推断出的 ECharts option 便于审查：

```bash
node scripts/make_chart_image.mjs --input data.md --output chart.png --save-option chart.option.json
```

## 支持的输入

JSON 输入可以是：

- 完整 ECharts option，例如包含 `series`、`xAxis`、`yAxis` 等字段的对象。
- `{ "option": { ... } }` 包装形式。
- 行对象数组：`[{ "month": "Jan", "sales": 120 }, ...]`
- 首行为表头的二维数组：`[["month", "sales"], ["Jan", 120]]`
- `{ "columns": [...], "rows": [...] }`
- `{ "labels": [...], "values": [...] }`

Markdown 输入使用第一张标准 Markdown 表格，并会尝试从第一个一级/二级标题读取默认标题。

## 常用参数

- `--chart-type auto|bar|line|pie|scatter`，默认 `auto`。
- `--title "标题"`，覆盖输入里的标题。
- `--width 1200 --height 800`，默认 `1200x800`。
- `--format png|svg|jpg|jpeg|webp`，未指定时从输出扩展名推断。
- `--x field`，指定分类字段。
- `--y field1,field2`，指定数值字段。
- `--name field --value field`，指定饼图字段。
- `--theme light|dark`，默认 `light`。
- `--save-option file.json`，保存最终 ECharts option。

## 输出要求

脚本成功后会在 stdout 输出 JSON，至少包含：

- `output`
- `format`
- `width`
- `height`
- `chartType`

如果脚本失败，读取 stderr 的真实错误并据实报告，不要声称图片已生成。
