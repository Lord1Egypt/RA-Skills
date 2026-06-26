# Changelog

All notable changes to Aegis Protocol are documented in this file.

---

## [0.12.6] - 2026-04-05

### Added
- **User configuration guidance** in SKILL.md
- **AI Agent Integration** section in README.md
- **Expected user questions** for AI agents
- **Configuration examples** for common setups

### Changed
- Enhanced: Limitations now include "You can configure" options
- Enhanced: FAQ includes AI agent guidance scripts
- Enhanced: Agent-readable documentation for better user guidance

### Fixed
- AI agents can now better guide users through setup

## [0.12.5] - 2026-04-05

### Added
- **Limitations section** in SKILL.md and README.md
- **FAQ section** in README.md
- **Log rotation** example in README.md
- **Cron setup** instructions

### Changed
- Clarified: Notifications are log-only (no push)
- Clarified: Manual cron setup required
- Clarified: CLI only (no WebUI)

### Fixed
- User expectations management

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.12.1] - 2026-04-05

### Added
- `send_heal_report()` - heal 汇总报告输出到日志
- 报告格式：Issues/Actions/Errors/Status

### Fixed
- heal() 返回值包含 `issues` 字段
- 配置文件验证错误处理

### Changed
- 汇总报告仅输出到日志 (无外部 API 调用)

---

## [0.12.0] - 2026-04-05

### Added
- **Whitelist 白名单功能**
  - `config.whitelist.sessions` - 跳过检测的 session
  - `config.whitelist.services` - 跳过告警的服务
- 完整类型注解 (>90% 覆盖)
- 异常分类系统 (AegisError, ConfigError, CheckError, RecoveryError)

### Fixed
- heal() 返回值结构不完整
- 移除未使用的 `send_heal_report()` (避免安全误报)
- notifications 默认禁用

### Changed
- 核心三问题检测 (Session/LLM/Service)
- 代码重写 (v0.5.0 → v0.12.0)
- 减少代码行数 (1034 → 971)

### Removed
- `openclaw.message` import (避免安全误报)
- 多平台通知系统

### Security
- 添加 SECURITY.md 安全文档
- 说明已知误报原因

---

## [0.11.0] - 2026-04-05

### Removed
- 通知功能 (避免安全误报)
- `send_notification()` 函数
- `send_heal_report()` 函数

### Changed
- notifications.enabled 默认 `false`

---

## [0.10.1] - 2026-04-05

### Fixed
- 禁用 `openclaw.message` import
- 添加 SECURITY.md 说明文档
- SKILL.md 添加 experimental-features

---

## [0.10.0] - 2026-04-05

### Added
- 多平台通知系统 (Telegram/Slack/Discord)
- `send_notification()` 函数
- `send_heal_report()` 函数
- heal 完成后自动发送汇总报告

### Changed
- notifications 配置项

---

## [0.9.0] - 2026-04-05

### Added
- **核心三问题检测**
  1. Session 卡死 → kill
  2. LLM 超时 → alert
  3. Service Down → restart

### Changed
- 简化问题分类 (7 种 → 3 种)
- 减少检查项 (8 项 → 5 项)
- 代码行数减少 (~950 → ~850)

---

## [0.8.0] - 2026-04-05

### Added
- 智能分类恢复系统
- `classify_issue()` 函数
- `get_recovery_action()` 函数
- 7 种问题类型映射

### Changed
- heal() 使用智能分类逻辑

---

## [0.7.1] - 2026-04-05

### Added
- SECURITY.md 安全文档
- SKILL.md security-note

### Fixed
- ClawHub suspicious 标记问题

---

## [0.7.0] - 2026-04-05

### Added
- 结果缓存系统 (ResultCache)
- TTL 5 分钟自动过期
- 缓存持久化到文件

### Changed
- check_disk() 使用缓存

---

## [0.6.6] - 2026-04-05

### Added
- Phase 2 代码质量改进完成
- 类型注解完善 (>90%)
- 测试覆盖率提升至 82%
- API 文档完善

---

## [0.4.0] - 2026-04-05

### Added
- **20 维系统监控**
  - 基础检查 (8 项): sessions/pm2/nginx/disk/memory/context/task_stall/loop
  - 扩展检查 (12 项): SSL/docker/network/cron/git/security/cpu/zombies/FD/connections/backup
- 健康度评分系统 (0-100)
- 自动恢复机制
- Healing Memory 策略记录

### Changed
- 重命名为 Aegis Protocol
- 版本从 v0.2.0 跳至 v0.4.0

---

## [0.2.0] - 2026-04-03

### Added
- 基础监控功能
- 8 维系统检查
- 简单恢复逻辑

---

## 版本命名规则

- **Major.Minor.Patch** (e.g., 0.12.1)
- **Major**: 破坏性变更 (未发布 1.0.0)
- **Minor**: 新功能 (向后兼容)
- **Patch**: Bug 修复

---

## 发布流程

1. 更新 `_meta.json` version
2. 更新 `SKILL.md` version
3. 更新本 CHANGELOG.md
4. Git 提交 + tag
5. GitHub 推送
6. ClawHub 发布

---

*Keep a Changelog - 记录每一次改变*
