# 本轮统一要求

## 目标

为视觉任务正式接入 `design_md` 协议与官方 `design.md` 实例。

## 必做项

- 更新 `ref/design-md/` 官方预设集合
- 在 `spec-template.yaml` 中新增 `design_md`
- 在协议文档、调研文档、设计文档、构建文档中同步 `design_md` 语义
- 让 `render_skill_from_spec.cjs` 生成 `references/design.md`
- 让 `validate_platform_skill.cjs` 校验设计资产

## 协议字段

- `design_md.enabled`
- `design_md.applies_to`
- `design_md.source_mode`
- `design_md.preset_id`
- `design_md.preset_ref`
- `design_md.user_provided_ref`
- `design_md.custom_style_notes`
- `design_md.official_library_ref`
- `design_md.prompt_user_to_use_first`
- `design_md.output_path`

## 验收条件

- `design_md.enabled: true` 时，渲染结果中存在 `references/design.md`
- 渲染结果中存在 `references/design-md/index.md`
- `SKILL.md` 明确提示用户先读设计入口
- 协议文档与主流程文档都承认 `design_md`
