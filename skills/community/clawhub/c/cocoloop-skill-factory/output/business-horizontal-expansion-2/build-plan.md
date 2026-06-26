# Build Plan

## Completed

- 新增 6 个业务域预设。
- 更新预设索引。
- 更新调研路由说明。
- 更新 `spec-template.yaml` 的 `domain_supplements`。
- 更新 PRD 中的任务域地图、预设治理、协议说明、补充块示例和质量说明。

## Verification

- 运行 builder 单元测试。
- 运行 builder 回归测试。
- 检查 Python CLI 编译。
- 确认没有生成 `__pycache__` 或 `.pyc` 残留。

## Follow-Up

- 后续可以为新增业务域增加更严格的 `domain_supplements` 字段校验。
- 后续可以让任务域路由器自动把自然语言 brief 映射到 20 个正式任务域。
- 后续可以为销售、人力、教育、法务、产品研究和活动社群补充参考 Skill 搜索关键词包。
