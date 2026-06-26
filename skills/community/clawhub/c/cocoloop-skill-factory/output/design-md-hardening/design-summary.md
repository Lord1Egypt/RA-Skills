# 设计摘要

## 设计目标

让视觉任务的设计输入成为正式协议，并在最终 Skill 中稳定落盘。

## 收口方案

- 新增顶层 `design_md` 协议块，统一服务网页、信息图、展示图、`.pptx`、HTML slides 等视觉排版任务。
- 最终 Skill 固定生成 `references/design.md` 作为默认设计入口。
- 同时复制 `references/design-md/` 预设库，允许用户在官方预设之间切换，或替换成自己的 `DESIGN.md`。
- 生成的 `SKILL.md` 与 `references/spec-summary.md` 明确提示先读 `references/design.md`。
- 平台校验在 `design_md.enabled: true` 时强制检查设计入口和预设目录。

## 官方预设集合

- IBM
- Stripe
- Notion
- Framer
- Figma
- Nothing
- Apple

## 设计取舍

- 没有把 `design_md` 塞进各任务域补充块，而是提升为顶层协议，避免同一逻辑在 `frontend_design` 和 `document_artifacts` 间重复维护。
- 没有把扩展参考删除，避免破坏现有本地文档资产。
- 没有引入图片、字体或 Figma 资源复制，保持这轮只处理 Markdown 级设计输入。
