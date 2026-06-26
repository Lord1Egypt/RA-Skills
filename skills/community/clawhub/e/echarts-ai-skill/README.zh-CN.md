# Echarts-AI-Skill

<div align="center">

**给你的 AI Agent 一项图表技能。**

把类似 **“用我的数据生成一个饼图”** 这样的请求，转换成稳定的 ECharts option 和可导出的 `HTML` / `SVG` 图表产物。

[![Release](https://img.shields.io/github/v/release/davaded/Echarts-AI-Skill)](https://github.com/davaded/Echarts-AI-Skill/releases)
[![License](https://img.shields.io/github/license/davaded/Echarts-AI-Skill)](./LICENSE)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![ECharts](https://img.shields.io/badge/ECharts-5.x-AA344D)](https://echarts.apache.org/)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111111)](./SKILL.md)

[English](./README.md) | 简体中文

</div>

---

## 为什么做这个 Skill

现在的 AI Agent 已经很会写代码、改文档、跑流程了。
但当用户开始说：

- “用我这份销售数据生成一个饼图。”
- “把这组周数据做成柱状图对比一下。”
- “帮我从这张表里选一个合适的图，然后导出到桌面。”
- “把这个图渲染成 SVG，我要放进报告里。”

Agent 背后通常还缺一个稳定的图表执行层。

`Echarts-AI-Skill` 就是这层能力。

它给 Agent 提供一条确定性的链路：
**数据请求 -> 图表推荐 -> ECharts option -> 可交付图表产物**。

## 你的 Agent 现在能做什么

### 内置自动推荐

对于常规表格型输入，当前自动推荐支持：

- `line`
- `bar`
- `pie`
- `scatter`

### 显式图表生成

如果请求里明确指定了 `chartType`，当前 builder 支持：

- `line`
- `bar`
- `pie`
- `scatter`
- `effectScatter`
- `radar`
- `funnel`
- `gauge`
- `heatmap`
- `treemap`
- `sunburst`
- `sankey`
- `graph`
- `candlestick`
- `boxplot`
- `parallel`
- `map`
- `lines`

### 图表类型对照表

| 类型 | 中文名称 |
| --- | --- |
| `line` | 折线图 |
| `bar` | 柱状图 / 条形图 |
| `pie` | 饼图 |
| `scatter` | 散点图 |
| `effectScatter` | 涟漪散点图 |
| `radar` | 雷达图 |
| `funnel` | 漏斗图 |
| `gauge` | 仪表盘 |
| `heatmap` | 热力图 |
| `treemap` | 矩形树图 |
| `sunburst` | 旭日图 |
| `sankey` | 桑基图 |
| `graph` | 关系图 |
| `candlestick` | K 线图 |
| `boxplot` | 箱线图 |
| `parallel` | 平行坐标图 |
| `map` | 地图 |
| `lines` | 线路图 / 迁徙线图 |

同时还支持：

- 交互式 `HTML` 预览导出
- 服务端渲染 `SVG` 导出
- 显式指定时支持 `desktop`、`home`、`~` 等友好路径
- [`SKILL.md`](./SKILL.md) 定义的 Codex 工作流

## 使用场景

### 1. 把分类汇总变成饼图

用户会说：

> 用我的分类汇总数据生成一个饼图。

这个 skill 会：

- 映射分类字段和值字段
- 构建合法的饼图 option
- 导出 HTML 预览或 SVG 图表产物

### 2. 把周度指标做成柱状对比图

用户会说：

> 把这组周表现数据做成柱状图对比一下。

这个 skill 会：

- 识别这是对比型数据
- 推荐 `bar`
- 生成稳定的 ECharts option

### 3. 把时间序列数据做成趋势图

用户会说：

> 用这份进度数据生成一个折线图。

这个 skill 会：

- 识别时间字段
- 推荐 `line`
- 导出可快速查看的预览结果

### 4. 显式生成更复杂的图表

用户会说：

> 用这些节点和连线生成一个桑基图。

这个 skill 会：

- 接收图表专属字段结构
- 生成 `radar`、`sankey`、`graph`、`gauge`、`heatmap` 等更复杂图表
- 保持生成链路是确定性的，而不是自由发挥式拼 option

### 5. 按用户习惯保存产物

用户会说：

> 把结果导出到桌面。

这个 skill 会：

- 支持 `desktop`、`home`、`~`
- 用更符合用户习惯的路径规则保存结果，而不是强迫用户写完整文件名

## 快速开始

```powershell
npm install
```

典型工作流：

```powershell
node dist/cli/recommend-chart.js --input examples\study-progress.request.json
node dist/cli/generate-chart.js --input examples\study-progress.request.json
node dist/cli/render-chart.js --input option.json --format html
node dist/cli/render-chart.js --input option.json --format svg
```

## Demo

- 产品化展示页：[`examples/product-demo.html`](./examples/product-demo.html)
- 学习趋势请求示例：[`examples/study-progress.request.json`](./examples/study-progress.request.json)
- 饼图请求示例：[`examples/pie-chart.request.json`](./examples/pie-chart.request.json)
- 雷达图请求示例：[`examples/radar.request.json`](./examples/radar.request.json)
- 仪表盘请求示例：[`examples/gauge.request.json`](./examples/gauge.request.json)
- 热力图请求示例：[`examples/heatmap.request.json`](./examples/heatmap.request.json)
- 桑基图请求示例：[`examples/sankey.request.json`](./examples/sankey.request.json)
- 关系图请求示例：[`examples/graph.request.json`](./examples/graph.request.json)

如果你想看更像产品展示页的效果，直接在浏览器中打开 `examples/product-demo.html`。

## 发布元信息

当前仓库已经补齐了更通用的技能发布元信息：

- [`SKILL.md`](./SKILL.md) 用于 Codex / OpenClaw 风格技能说明
- [`manifest.yaml`](./manifest.yaml) 用于发布导向的 metadata
- [`agents/openai.yaml`](./agents/openai.yaml) 用于 OpenAI 风格技能 metadata

如果你要发布到 ClawHub / OpenClaw，剩下的主要步骤就是在登录对应平台 CLI 后，从仓库根目录执行发布命令。

## 面向 Agent 的请求示例

```json
{
  "title": "Category sales share",
  "chartType": "pie",
  "dataset": [
    { "category": "Books", "amount": 3200 },
    { "category": "Courses", "amount": 5100 },
    { "category": "Templates", "amount": 1700 }
  ],
  "categoryField": "category",
  "valueField": "amount"
}
```

这个示例更接近用户真实会说的话：

> 用我的分类汇总生成一个饼图。

## 输出规则

- `--out`：写入精确文件路径
- `--out-dir`：写入指定目录，并自动使用默认文件名
- 当用户明确要求这些位置时，输出路径支持 `desktop`、`home`、`~`
- 如果没有提供路径，默认输出到当前工作目录

默认文件名：

- `recommend` -> `spec.json`
- `generate` -> `option.json`
- `render --format html` -> `preview.html`
- `render --format svg` -> `preview.svg`

## 项目结构

```text
src/
  cli/      命令行入口
  core/     推荐、构建和渲染核心
  types/    请求与规格类型
examples/   示例输入与展示页面
agents/     跨平台技能 metadata
SKILL.md    Codex Skill 说明
manifest.yaml 发布导向 metadata
```

## 范围

### 当前版本

- 结构化图表输入
- 常见图表自动推荐
- 更广的显式 `chartType` 支持
- HTML 与 SVG 导出
- Codex Skill 工作流
- 面向技能生态的通用发布元信息

### 下一步

- 自然语言转 `ChartRequest`
- 更细的图表类型校验规则
- 图表解释与修正工作流
- MCP 服务封装

## 许可证

本项目采用 [MIT License](./LICENSE)。
