# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-03-03

### Added
- 单文件 gateway_watchdog.py，使用 argparse 子命令
- 自动检测 Windows/Linux 系统
- 自动查找 openclaw 命令路径
- start/stop/status/restart 子命令
- 连续失败自动重启 Gateway

### Features
- `start` - 启动 watchdog
- `stop` - 停止 watchdog 进程
- `status` - 查看 watchdog 和 Gateway 状态
- `restart` - 重启 Gateway

### Files
- gateway_watchdog.py - 主脚本
- README.md - 说明文档
- .gitignore - 忽略本地文件
