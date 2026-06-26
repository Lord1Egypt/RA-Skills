# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-03-31

### Added
- **四类记忆分类系统** - 引入 user / feedback / project / reference 四种记忆类型
  - 每种类型有明确的作用域、保存时机、最佳实践
  - 规范的记忆格式和目录结构
- **Feedback 双向记录** - 同时记录负面纠正和正面确认
  - 解决"只记错误不记成功"的问题
  - 包含 Type / Why / How to apply 结构化格式
- **记忆索引规范** - MEMORY.md 索引格式指导
  - 每条索引 <= 150 字符
  - 目录结构建议

### Improved
- memory_search 增加 type 参数，支持按类型筛选
- memory_write 增加 type 参数，支持指定记忆类型

---

## [1.0.2] - 2026-03-17

### Changed
- 优化描述文案（基于 Claude 改进版本）
- "向量搜索"改为"支持搜索"（更通用）
- 统一中英文术语

---

## [1.0.1] - 2026-03-17

### Added
- 增加降级方案说明：未配置 Ollama 时自动降级为关键词匹配
- 优化 flushMode 配置说明
- 增加注意事项（并发写入、权限等）

---

## [1.0.0] - 2026-03-17

### Added
- 完整的记忆系统框架
- 文件系统存储（Markdown 格式）
- 向量语义搜索（Ollama + nomic-embed-text）
- 关键词搜索（降级方案）
- 自动加载机制
- Memory Flush 机制
- 群组隔离记忆

---

**首发版本**: 团宝 (openclaw)
