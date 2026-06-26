# Changelog

## [1.2.0] - 2026-03-31

### Added
- **AutoDream 自动整合系统** 🌙
  - 定时触发记忆整合
  - 基于时间（默认24小时）和会话数（默认3个）触发
  - 自动扫描、清理、更新记忆
  - 新增 `memory_dream` 和 `memory_dream_status` 工具
  - 新增 `onHeartbeat` hook 支持
- 整合 Prompt 生成器
- 整合状态持久化（`.auto-dream-state.json`）

### Improved
- 工具函数增加 AutoDream 相关功能
- 配置结构优化，支持 `autoDream` 子配置

---

## [1.1.0] - 2026-03-31

### Added
- **四类记忆分类系统** - 引入 user / feedback / project / reference
- **Feedback 双向记录** - 同时记录 negative 和 positive feedback
- `memory_search` 增加 `type` 参数筛选
- `memory_write` 增加 `type` 参数

---

## [1.0.2] - 2026-03-17

### Changed
- 优化描述文案
- "向量搜索"改为"支持搜索"

---

## [1.0.0] - 2026-03-17

### Added
- 完整记忆系统框架
- 文件系统存储
- 向量语义搜索
- 关键词搜索（降级方案）
- 自动加载机制
- Memory Flush 机制
- 群组隔离记忆

---

**作者**: 团宝 (openclaw)
