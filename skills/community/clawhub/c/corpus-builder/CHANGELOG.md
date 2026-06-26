# 变更日志

所有重要变更将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.1.0] - 2026-04-01

### Added
- **代码模块化** - 将单文件拆分为 6 个模块（chunker/annotator/embedder/store/utils）
- **单元测试套件** - 18 个测试用例，覆盖率 100%
- **详细文档** - 添加 references/ 目录（annotation-schema.md, troubleshooting.md）
- **智能导入系统** - 支持脚本和模块两种运行方式

### Improved
- **代码可读性** - 单文件从 1480 行降至~400 行/模块
- **可维护性** - 模块化设计，职责清晰
- **SQLite3 兼容性** - 自动修复 pysqlite3 导入问题
- **正则表达式优化** - 简化章节匹配逻辑

### Fixed
- **章节识别** - 修复正则表达式无法匹配中文数字的问题
- **导入顺序** - 修复 E402 模块导入顺序问题
- **未使用导入** - 清理 F401 未使用导入
- **代码规范** - ruff check 0 问题

### Changed
- **移除检索功能** - 检索功能已移至 corpus-search skill
- **版本升级** - 从 1.0.3 升级到 1.1.0（重大改进）

## [1.0.3] - 2026-04-01

### Fixed
- 修复未使用导入（glob, hashlib）
- 修复变量命名冲突（field 与 dataclass field）
- 修复裸 except 为 except Exception

### Changed
- 代码质量优化，ruff check 全部通过

## [1.0.2] - 2026-04-01

### Security
- **删除全局 OpenClaw 配置读取** - 不再访问 `~/.openclaw/openclaw.json`
- API Key 仅通过环境变量传递
- 添加安全说明文档

### Changed
- 明确说明 LLM 集成和 API 要求
- 删除"完全离线"虚假宣传

## [1.0.1] - 2026-04-01

### Added
- 添加 pyproject.toml（现代 Python 标准）
- 添加完整 README.md
- 支持 `pip install .` 安装

### Changed
- 改进安装体验
- 添加详细使用示例

## [1.0.0] - 2026-03-28

### Added
- 初始版本发布
- 智能分块功能
- 10 维度 AI 标注
- ChromaDB 向量存储
- 语义检索功能
- 断点续传功能
- 内存监控功能
- 双模式标注（LLM/规则）
