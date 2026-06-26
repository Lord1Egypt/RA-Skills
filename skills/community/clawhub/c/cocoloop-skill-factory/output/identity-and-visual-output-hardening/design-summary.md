# 设计摘要

## 设计选择

- 正式名称使用 `skill_identity.slug`。
- 展示名称使用 `skill_identity.display_name`。
- 保留 `skill_identity.id` 与 `skill_identity.name` 作为兼容字段，不再让它们承担主语义。
- 名称 gate 放到 `research_gate.skill_identity`，由双源去重结果驱动。
- 视觉输出判断放到 `output_profile`，不把它混进 `design_md` 本身。

## 这样设计的原因

- 名称身份和展示名属于结果协议，不应该继续依赖推导。
- 去重检查属于调研阶段 gate，不应该等到发布时才暴露冲突。
- 是否包含可视化输出是更上游的事实判断，`design_md` 只是它带来的设计输入约束。
- 继续保留旧字段，可以避免当前样例和历史产物一次性断掉。

## 这轮不做的事

- 不新增独立发布器
- 不改写视觉叙事层本身
- 不自动替用户选择 `design_md.source_mode`
