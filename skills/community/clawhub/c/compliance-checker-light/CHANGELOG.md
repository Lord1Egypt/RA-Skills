## [v1.1.6] - 2026-03-24

### Added
- 新增 OpenClaw SecretRef 配置支持模块 (`secret_ref.py`)
- 支持三种 SecretRef 来源：env、file、exec
- 新增 `CheckerConfig.from_secret_ref()` 方法替代 `from_env()`

### Changed
- **BREAKING**: 移除所有环境变量读取逻辑（`os.getenv`）
- **BREAKING**: 配置必须通过 `secrets` 字典传入
- SKILL.md: 移除 `env_required`/`env_optional`，改为 `secrets` 声明
- _meta.json: 移除 `requires.env`，添加 `secrets` 字段
- README.md: 更新配置说明为 SecretRef 方式
- docs/: 更新架构文档和开发指南

### Security
- 符合 ClawHub 安全规范，避免被标记为危险
- 所有敏感配置通过 OpenClaw SecretRef 机制注入

---

## [v1.1.5] - 2026-03-23

### Added
- SKILL.md: 增加 OCR 安装说明（local-ocr / cloud-ocr / all）

### Changed
- SKILL.md: 删除残留的 `.env` 文件和 CLI 相关表述
- pyproject.toml: 删除 CLI 入口和 CLI Tool 描述

---

## [v1.1.4] - 2026-03-23

### Fixed
- 修复 visual（视觉检查）API Key fallback 未生效的问题

---

## [v1.1.3] - 2026-03-23

### Fixed
- _meta.json: 修复 `requires.env` 只包含必需的 `LLM_API_KEY`，与 SKILL.md 保持一致
- _meta.json: 添加 `requires.bins` 字段声明依赖的二进制文件
- _meta.json: 统一 `install` 字段为 `pip install compliance-checker`

---

## [v1.1.2] - 2026-03-22

### Changed
- SKILL.md: 环境变量声明改为 env_required/env_optional 分离，仅 LLM_API_KEY 为必需
- SKILL.md: 移除路径探测权限，明确禁止 Agent 自主探测文件系统
- SKILL.md: 新增数据隐私与合规声明章节
- _meta.json: 添加 type: cli-tool 声明
- README.md: 清理过时的 MCP Service 相关内容，更新为 CLI Tool 定位

---

## [v1.1.0] - 2026-03-22

### Added
- 新增 RAG 检索模块，支持法规检索增强时效性检查
- 新增 CLI 命令行工具支持
- 添加示例文档 (Examples/)

### Changed
- 重构时效性检查器，增强日期解析逻辑
- 改进 OCR 引擎功能
- 重构项目结构，优化 OpenClaw 扫描报告

### Fixed
- 修复 OpenClaw 扫描报告的元数据和安全问题

---

## [v1.0.0] - 2026-03-15

## What's Changed

- ci: 优化 Docker 构建工作流和 Dockerfile by @evob
- 更新测试文件 by @evob
- 1.格式修改；2.添加测试文件 by @evob
- test: 修复 TimelinessChecker 断言和 Config 配置项测试 by @evob
- refactor: 优化 MCP 提示词并现代化 Dockerfile 配置 by @evob
- refactor: 重构为 Clean Architecture 五层架构 by @evob
- fix(checkers): 修复状态码大小写不匹配问题 by @evob
- ci: fix CI workflow - add pytest-cov and revert safety command by @evob
- ci: add coverage configuration to exclude non-business files by @evob
- ci: update safety command from check to scan by @evob
- test: add comprehensive unit test suite by @evob
- chore: 删除多余的 CI/CD 相关文件 by @evob
- refactor(ci): 重构 CI/CD 为三个独立工作流 by @evob
- feat(ci/cd): 添加完整的 CI/CD 流水线配置 by @evob
- feat: 完善合规检查服务功能和文档 by @evob
- fix(visual): 修复视觉模型调用逻辑和不可用状态处理 by @evob
- Initial commit: Compliance Checker MCP Service by @evob
**Full Changelog**: https://github.com/evob-z/compliance_checker_light/compare/...v1.0.0

# Changelog

All notable changes to this project will be documented in this file.

