# 对话侧推荐流程

1. 向用户确认或补全关键信息（活动名称、时间、地点、邀请对象、风格关键词）；若已说清可跳过追问。
2. 将信息合并为一段自然语言需求，执行 CLI `create`（`--prompt`）。
3. 将 stdout 中的 `previewUrl`、`editUrl` 返回给用户；说明编辑链接登录后可改。
4. **（可选）文案**：`editable-text` → 大模型检查 JSON → 按需 `update-text`（从可编辑文本结果取 `page_id`、`element_id`）。
5. **（可选）换图**：`body-images` →（如需新图）`upload` → `replace-body-image`。

`scene_id` 即 `create` 返回 JSON 中 `data.id`。
