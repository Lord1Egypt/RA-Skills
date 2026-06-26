# Structured Visual Storytelling 调研摘要

## 任务目标

把当前已经验证有效的 PPT / 网页信息图设计方法，抽象成 `cocoloop-skill-factory` 可复用、可批量生产的共享原子能力。

## 当前问题

现有经验已经证明，单纯把内容拆成页面并不足以稳定产出高质量视觉稿。

视觉叙事类 Skill 还需要同时控制：

- 内容结构是否先被压成稳定叙事单元
- 是否先读取 `design.md`
- 页面是否有清楚的文字层级
- 页面是否显式包含信息图元素
- 最终产物是否符合目标载体的可编辑性与展示要求

这些规则过去分散在 `presentation-generation`、`infographic-generation`、测试样例和设计预设里，缺少统一编排层。

## 调研结论

适合抽象的不是 “PPT 生成” 本身，而是更高一层的 “结构化视觉叙事产物生成”。

这一层应当只处理共享规则：

- 先结构化内容，再设计排版
- 强制接入 `design_md`
- 强制文字层级
- 强制至少一种信息图元素
- 根据产物类型切换 adapter

## 支持的首批产物

- `ppt`
- `web_infographic`
- `showcase_graphic`
- 后续可扩展到 `poster`
- 后续可扩展到 `report_page`

## 结论

新增原子能力 `structured-visual-storytelling`，并把 `presentation-generation`、`infographic-generation` 视作 adapter，而不是各自独立发明一套流程。
