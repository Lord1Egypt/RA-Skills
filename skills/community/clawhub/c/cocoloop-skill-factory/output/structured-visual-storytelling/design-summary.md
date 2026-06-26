# Structured Visual Storytelling 设计摘要

## 能力定义

`structured-visual-storytelling` 是一个面向视觉叙事产物的共享原子能力。

它不直接等于 PPT、网页信息图或海报生成器。

它负责把任何视觉叙事任务先拉回同一条生产线，再交给具体 adapter 输出。

## 共享生产线

### 1. 结构化内容

先把输入材料压成 `story_units`，例如：

- cover
- context
- problem
- method
- evidence
- result
- comparison
- closing

### 2. 读取设计背景

所有视觉叙事类任务优先走 `design_md`。

默认读取官方预设，也允许用户提供自己的设计文件。

### 3. 强制文字层级

至少覆盖以下层：

- kicker
- headline
- summary
- body
- metric
- annotation

### 4. 强制信息图元素

至少要求一种信息图结构，常用类型包括：

- process_flow
- comparison_block
- metric_cards
- matrix
- timeline

### 5. 选择 adapter

共享层不负责具体版式语法。

它只决定产物类型，再交给：

- `ppt`
- `web_infographic`
- `showcase_graphic`

### 6. 验收

共享验收规则包括：

- 不能是纯文本堆砌
- 页面必须存在清楚的文字层级
- 页面必须出现信息图元素
- 结果必须符合目标载体的可编辑或可展示要求

## 协议设计

在 `spec.yaml` 顶层新增 `visual_storytelling`：

- `enabled`
- `artifact_family`
- `story_units`
- `text_hierarchy`
- `infographic_elements`
- `output_adapters`
- `editability_target`
- `validation_checks`

## 结论

以后只要任务属于视觉叙事产物，factory 就应该先走 `structured-visual-storytelling`，再进入具体 adapter。
