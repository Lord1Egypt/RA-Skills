# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-03-07

### Added
- 初始版本发布
- Bash 版本 (`clash-switch.sh`)
- 增强版 Bash (`clash-switch-v2.sh`) - 支持日志和状态追踪
- PowerShell 版本 (`clash-switch.ps1`) - Windows 支持
- Python 跨平台版 (`clash-switch.py`) - 推荐使用
- OpenClaw Skill - 支持 `/clash` 命令
- 配置示例文件
- 完整的 README 文档
- GitHub Actions 部署配置

### Features
- 健康检查 (测试 Telegram/Google/Anthropic)
- 自动切换到最佳节点
- 区域优先 (新加坡/日本/香港/美国)
- 手动切换指定节点
- 定时任务支持
- 日志记录
- 状态追踪

### Platforms
- ✅ Linux / macOS (Bash)
- ✅ Windows (PowerShell)
- ✅ 跨平台 (Python)
- ✅ OpenClaw Skill

---

## [Unreleased]

### Planned
- [ ] 添加通知支持 (Telegram/Discord 通知)
- [ ] Web 界面
- [ ] 统计面板 (节点使用时间/流量)
- [ ] 支持更多测试目标
- [ ] 智能学习 (根据使用习惯自动选择节点)
