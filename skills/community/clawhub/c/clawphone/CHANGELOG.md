# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-03-13

### Added
- **Direct P2P 模式** - 内置 WebSocket 服务器，无需 ClawMesh 即可通信
- **适配器模式** - 支持多网络层（ClawMesh / Direct），运行时切换
- **号码簿数据库** - SQLite 本地存储，支持 alias → phone_id → address 映射
- **自动号码生成** - 13 位随机数字（1000000000000-9999999999999）
- **事件回调机制** - `on_message` 事件驱动接收
- **状态管理** - `set_status("online"/"away"/"offline")`
- **完整示例** - `examples/direct_demo.py` 和 `examples/quick_demo.py`
- **单元测试** - `tests/test_clawphone.py`, `tests/test_p2p_simple.py`

### Changed
- 升级 ClawMesh 依赖到 >= 1.0.0（Phase 1-3 完成）
- 数据库结构扩展，增加 `address` 字段用于 Direct 模式

### Fixed
- DirectAdapter 发送回调同步问题（call() 不再返回 coroutine）
- 早期版本的手動綁定 API 标准化

### Known Issues
- 无离线消息缓存（Phase 2 规划）
- 无群聊支持（Phase 2 规划）
- 无自动号码发现（Phase 2 规划）

---

## [1.0.0-beta] - 2026-03-10

### Added
- 初始发布
- 基础 ClawMesh 适配（依赖外部网络）
- register(), call(), lookup() 核心功能
