# 构建计划

1. 更新 `spec-template.yaml`，补齐名称身份字段、视觉输出字段和新 gate。
2. 更新 `_spec_common.cjs`，让显式 slug 与 display name 成为首选来源。
3. 更新 `render_skill_from_spec.cjs`，接入新 gate，并把视觉输出要求写进 render 结果。
4. 更新 `validate_platform_skill.cjs`，把名称身份和视觉输出做成硬校验。
5. 更新 `search-registry.py`，支持精确 slug 检查。
6. 同步主流程文档、协议文档和样例 spec。
7. 用当前目录下的 `spec.yaml` 跑一次 render 与 validate。
