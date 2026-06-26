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

- 后续可以为每个业务域增加 `domain_supplements` 的完整字段校验。
- 后续可以让任务域路由器自动把自然语言 brief 映射到这 14 个域。
- 后续可以为内容、知识库、数据报告等业务域增加参考 Skill 搜索关键词包。
