# 名称身份与视觉输出加固研究摘要

## 已确认结论

- 现有协议只有 `skill_identity.id` 与 `skill_identity.name`，还没有正式 slug 和 display name。
- 现有渲染链通过推导生成 slug 与展示名，无法把名称收口变成硬门槛。
- 现有视觉产物只在 `design_md.enabled: true` 时才会生成 `references/design.md`，缺少“包含任何可视化输出就必须带设计模板”的机械约束。
- 现有搜索入口已经同时覆盖 `cocoloop` 与 `clawhub`，适合继续承担 slug 去重检查。

## 这轮研究决定补齐的协议

- `skill_identity.slug`
- `skill_identity.display_name`
- `research_gate.skill_identity`
- `output_profile.has_visual_output`
- `output_profile.visual_output_types`

## 需要同步落地的层

- 协议模板
- render builder
- validator
- 搜索入口
- 主流程文档
- 样例 spec
