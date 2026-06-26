# Changelog

## [1.0.1] - 2026-05-20
### Changed
- 新增 `manifest.json`，为 WorkBuddy 等自动化平台提供稳定的 JSON 参数定义。
- 将 `SKILL.md` 中的示例调用方式从 XML 调整为 JSON，并补充 UTF-8/转义要求。
- 增加默认 `compact` 输出规范，减少自动评测中的超时风险。
- 收紧模板与示例输出长度，默认 FAQ 数量从 10 条下调为 5 条。
- 移除仓库中的 `.DS_Store` 二进制文件，并新增 `.gitignore` 避免隐藏文件再次影响打包与编码。

## [1.0.0] - 2026-05-11
### Added
- 初始化项目为简化版的“豆包 GEO 效果评估 Skill”。
- 确立了简化的评估目标，专注于核心文本的理解度和推荐度。
- 添加了核心评估 prompt (`prompts/audit.md`, `prompts/scoring.md`)。
- 添加了标准化的输出报告模板 (`templates/doubao_geo_audit_report.md`)。
- 添加了具体的示例输入与输出 (`examples/example_input.md`, `examples/example_output.md`)。
- 完善了 `SKILL.md` 及 `README.md`。
- 移除了后端的冗余代码与配置文件，完全契合纯文本输入分析的 MVP 范式。
