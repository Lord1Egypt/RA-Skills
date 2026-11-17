---
name: visual-delivery-standard
description: Standardize visual design and layout for any client-facing deliverable (reports, dashboards, PPT, Word, Excel, PDF, HTML). Applies a Morandi business palette (steel-blue + ochre), meeting-card layout, mixed chart types, P0/P1/P2 prioritization, and strict data discipline. Use when producing or reviewing purchasing / supply-chain materials, dashboards, or any document that must look polished, consistent, and on-brand.
---

# 通用看板视觉交付标准 (Visual Delivery Standard)

## Overview

本 skill 把「沉稳、高级、商务克制」的版式与配色要求固化成一套可复用的交付标准。适用于报告、看板、PPT、Word、Excel、PDF、HTML 等所有对外交付物，保证跨任务、跨文件的视觉一致性。

配套参考文件（详见 `references/`）：
- `通用视觉交付标准.md` — 完整细则 + 禁止清单 + 自检清单
- `配色规范_Morandi商务.md` — Morandi 配色 token（钢蓝 + 赭石）

## When to Use

- 需要产出 / 改造任何对外交付物（看板、月报、定标报告、合同对比、供应商矩阵等）
- 用户要求「按统一视觉标准 / 商务风 / 高级感 / 配色一致」输出
- 交付前做版式与配色 Review 时

## How to Apply

### 1. 配色（必须严格遵循，不自行新增颜色）

主色 钢蓝 `#2E4A62`（页头/表头/KPI 左边框/选中态）；钢蓝浅 `#42596E`（仅页头渐变中段）；强调 赭石 `#B5791F`（章节竖条/关键数值/hover）。
辅助：雾青 `#8FA3AD`、紫灰 `#7A6E80`、卡其 `#C2B49A`。
语义：正向/通过/稳定 → 鼠尾草绿 `#6E8471`；负向/风险/终止 → 砖红（低饱和）`#A8524A`。
版式：页面背景 `#F7F6F3`、卡片 `#FFFFFF`、边框 `#E4E1DB`、轨道 `#EFEDE8`/`#F2F0EB`、正文 `#2B2B2B`、次要文字 `#4A5A6A`。
页头渐变固定 `linear-gradient(116deg,#2E4A62 0%,#42596E 52%,#7A6E80 100%)`；警示框底 `#FBF4E6` / 边 `#E8D9B8`。
图表序列色（循环）：`#2E4A62 #B5791F #8FA3AD #7A6E80 #C2B49A #6E8471 #A8725C #5C7480 #9E8B6E #4E6070`。
等级色（全局统一）：1级 `#A8524A`、2级 `#B5791F`、3级 `#8FA3AD`、4级 `#C2B49A`。
禁用：粉红/玫红/高饱和红/荧光色/彩虹渐变；除页头外不要大面积渐变。

### 2. 字体与层级（全篇 ≤4 级）

| 层级 | 屏幕 | 打印 | 颜色 | 用途 |
|---|---|---|---|---|
| H1 | 20-22px | 16-18pt | `#2E4A62` | 文档标题 |
| H2 | 15-16px | 13-14pt | `#2B2B2B` + 赭石竖条 | 一级章节 |
| H3 | 13.5-14px | 11-12pt | `#2E4A62` | 二级章节 |
| 正文 | 13.5px | 10.5-11pt | `#2B2B2B` | 正文 |
| 注释 | 11.5-12px | 9pt | `#4A5A6A` | 口径/来源/脚注 |

同一层级字号、颜色、行高必须一致，禁止随手加大的字号。数字用 `tabular-nums` 保证对齐。

### 3. 版式与密度（meeting-card 风格）

- 卡片：圆角 9px、1px `#E4E1DB` 边框、白底、内边距 15px 17px、行高 1.62、hover `#FAF9F7`
- 禁止：散落加粗、密横线分隔、条目长度参差、文字重叠、图表类型混杂堆砌
- 禁止表格跨页断行；长表要么压到一页、要么显式拆表并重复表头
- 卡片等高对齐，同组 KPI/图例/单位对齐基准线；留白优先，外边距 8%-12%，卡片间距 12-14px
- KPI 卡统一：左侧 3px 主色竖条，数值 22-24px 半透明主色，标签 12px 次要色

### 4. 图表规范

- 同一份材料混合 ≥2-3 种图（环形/柱状/堆叠条/雷达/横道图/评分表），不要通篇柱状图
- 饼/环形扇区 ≤6，超出归「其他」；数值直接在图旁或条尾标注
- 单位写在标题/轴名，不每个点重复；每张图标题写「结论」而非「XX图」
- 甘特/进度图：含里程碑、周末阴影、当前日期线，条尾标注工期+DDL
- 禁止 3D、立体、拟物阴影、撞色渐变

### 5. 表格规范

- 表头深底白字、无纵向分割线、横向分割线浅色 1px
- 数字右对齐+统一千分位/小数位；文本左对齐
- 对比数据一律表格双列并排，不用大段文字描述差异
- 状态列用 pill 标签（圆角 12-14px、10-12px 字号）

### 6. 内容结构与优先级

- 结论先行：首屏即「结论 + 关键数字」
- 结论 → 细节 → 附录；每个模块有可执行结论（谁/做什么/何时/依据数据）
- 标注 P0/P1/P2：P0 重大-阻塞（砖红）、P1 重要-需决策（赭石）、P2 优化-可延后（雾青）

### 7. 数据纪律（红线）

- 所有数据来自给定原始资料，禁止估算/推测/补全
- 估算须先确认 + 视觉隔离（虚线框/斜体）+ 明确标注
- 派生数值展示过程/公式，Excel 用公式驱动，禁止硬编码结果
- 口径不清 → 用警示框 `#FBF4E6/#E8D9B8` 明示并给代理口径
- 数据冲突不自动择优，并列呈现并进入「待核实」区域

### 8. 导出与交付

- PDF：A4、≤7 页（超界先压附录或拆分），版式不走形优于截图
- Excel：公式驱动 + 独立勾稽验证页（自动 PASS/FAIL）
- HTML：单文件、内联样式、无外部 CDN、响应式 + 打印样式（`@media print` 隐藏侧栏、白底、`page-break-inside:avoid`）；折叠区用 `<details>`，日志/口径/附表默认收起；锚点必须命中存在，JS 通过语法检查，断网可打开；图表用手写 SVG
- 图片：PNG/JPEG 透明底优先，≥150dpi

## Usage Pattern

代理新任务时：把「配色 + 版式 + 数据纪律 + 导出」四节作为约束整段写入任务 prompt；交付前按 `references/通用视觉交付标准.md` 第四章的 12 项自检清单逐项核对并回报结果。

## References

- `references/通用视觉交付标准.md` — 完整标准（细则 + 禁止清单 + 自检清单）
- `references/配色规范_Morandi商务.md` — 可直接复制的配色提示词 + CSS/JS token
