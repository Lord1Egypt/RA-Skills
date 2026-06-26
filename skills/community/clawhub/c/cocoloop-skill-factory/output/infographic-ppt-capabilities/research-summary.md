# Infographic And PPT Capabilities - 研究摘要

## 目标

把“信息图生成”和“PPT 生成”补成 `skill-factory` 的正式原子能力，并明确它们在主流程中的推荐执行面。

## 本次核实对象

- 当前原子能力目录
- 当前预设目录
- 本地 `imagegen` skill
- 本地 `slides` skill

## 核实结果

### 1. 信息图能力已有可复用基线

本地 `imagegen` skill 已明确覆盖：

- `infographic-diagram`
- 图像生成
- 图像编辑
- 单张视觉成品

这意味着信息图不需要从零定义执行面，重点是把“位图成品 vs 可编辑版式”的判断写清楚。

### 2. PPT 能力已有可复用基线

本地 `slides` skill 已明确覆盖：

- `.pptx` 生成和修改
- PptxGenJS
- 渲染检查
- 溢出检测
- 字体检测

这意味着 PPT 生成方向已经有明确最佳实践，重点是把它正式接入 `document_artifacts` 主域和调研流程。

## 研究结论

这两项能力不需要新开任务域，更适合作为：

- `frontend_design` 下的信息图补充能力
- `document_artifacts` 下的 PPT 补充能力

同时，它们都需要单独原子能力文档，方便后续设计阶段直接引用。
