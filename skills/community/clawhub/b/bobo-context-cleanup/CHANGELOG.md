# Changelog

## [0.3] - 2026-03-06 20:47 (Asia/Shanghai)

### Changed
- 调整发布标题为英文：`Context Cleanup`。
- 优化 `description` 为中英双语，增强可读性与检索触发信息。
- `metadata.version` 升级至 `0.3`，并更新 `updatedAt`。

## [0.2] - 2026-03-06 20:34 (Asia/Shanghai)

### Added
- 新增 `references/policy.md`，规范安全策略与执行顺序。
- 脚本支持 `--dry-run`、`--yes`、`--json` 参数。

### Changed
- 重写 `cleanup.sh`，修复计数与日期判断可靠性问题。
- 统一流程为 analyze → plan → confirm → archive。
- `metadata` 增加 `version` 与 `updatedAt`。

## [0.1] - 2026-03-06 16:20 (Asia/Shanghai)

### Added
- 初版 `context-cleanup` 技能与 `cleanup.sh`。
- 支持上下文分析、清理计划与归档。
