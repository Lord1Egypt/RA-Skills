# Changelog

## [1.0.1] - 2026-03-23

### Fixed
- 🔧 修复 Cron 服务检测逻辑（支持 crond/cron 多模式）
- 🔧 修复 OpenClaw Gateway 检测（进程名 + 端口双重验证）
- 🔧 兼容 Python 3.6（subprocess.Popen 替代 capture_output）

### Changed
- 📝 Cron 检测失败时返回 warning 而非 error
- 📝 Gateway 检测失败时返回 warning 而非 error

---

## [1.0.0] - 2026-03-23

### Added
- ✨ L1/L2/L3 三级系统健康检查
- ✨ 心跳机制（智能输出）
- ✨ 国际化支持（en/zh-CN）
- ✨ 零外部依赖设计
