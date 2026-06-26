# Changelog

All notable changes to Agent Communication Hub are documented here.

## [Unreleased]

### Fixed
- **FTS5 JOIN NULL 修复**: `recallMemory` 和 `deleteMemory` 中 FTS5 表 JOIN 条件不再因 NULL title 失效
- **db.ts 硬编码路径移除**: 删除 WorkBuddy 特定路径回退，仅依赖 `DB_PATH` 环境变量或 CWD
- **stdio 日志统一**: `console.error` 替换为结构化 logger

### Changed
- **metrics O(1) 查找**: Counter/Histogram 从线性数组改为 `Map<string, T>`，消除 O(n) 遍历
- **类型安全 DB 助手**: 新增 `getRow<T>` / `getAllRows<T>` / `getCount`，减少 `as any` 58→45 处

### Added
- **memory 模块单元测试**: 26 个测试覆盖 store/recall/list/delete 全部路径
- **CHANGELOG.md**: 首次创建

### Docs
- **README 文档链接修复**: 移除已删除的 API_REFERENCE/evolution-engine/hermes-integration 引用
- **Docker 示例修正**: 增加 `-v` 卷挂载和 `DB_PATH` 环境变量
- **SKILL.md 版本对齐**: v2.5.5 → v2.4.5，与 package.json 一致

### Housekeeping
- **.gitignore**: `coverage/` 目录加入忽略列表并从 git 跟踪移除

## [2.4.5] — 2026-05-22

### Changed
- Docker 多阶段构建优化，减小镜像体积
- 统一全部文档中工具数量描述为 53

### Added
- DB 分裂三层防护系统（检测 + 自动合并 + 看门狗自愈）
- Live demo 页面（`demo/index.html`）

### Fixed
- Node v24 兼容性（better-sqlite3 rebuild）
- tsconfig.json rootDir 修复 Docker 构建路径问题
- 敏感词清理（v2.4.4）

## [2.4.1] — 2026-05-17

### Changed
- 统一错误码体系（HubError）
- 清理无用代码和冗余导入

### Fixed
- 测试文件中的硬编码路径替换为 `__file__` 相对路径
- SKILL.md 去敏通过 ClawHub 安全扫描

## [2.4.0] — 2026-05-16

### Added
- Phase 5a: RBAC 细化（group_admin 角色）
- Phase 5a: 审计日志哈希链防篡改
- Phase 5a: 信任评分自动计算
- Phase 4b: 依赖链（DFS 环检测）
- Phase 4b: 并行组（ParallelGroup）
- Phase 4b: 质量门（QualityGate）
- Phase 4b: 交接协议（Handoff）
- Phase 4b: 分级策略审批（Tier 1-3）
- Phase 3: Evolution Engine（经验共享 + 策略审批 + 反馈闭环）
- 共享记忆三级作用域（private/group/collective）
- FTS5 中文分词（N-gram）
- SSE 实时推送（客户端去重）
- Python SDK（68 方法，零外部依赖）
- TypeScript SDK（35 公共方法）
- Prometheus + Grafana 可观测性栈

### Security
- RBAC 4 级（public → member → group_admin → admin）
- Token SHA-256 哈希存储
- 审计哈希链保证日志不可篡改
- CORS 白名单制
- 安全头（X-Frame-Options, CSP, HSTS, X-XSS-Protection）

## [2.3.2] — 2026-05-08

### Added
- 文件传输（upload / download / list）
- `get_db_stats` / `archive_data` 数据库维护工具

### Fixed
- 消息去重模块边缘情况修复

## [2.3.0] — 2026-05-06

### Added
- MCP Streamable HTTP Transport 支持
- stdio MCP 传输入口
- 速率限制器
- 邀请码注册机制
- Hermes 集成指南

### Changed
- 工具数扩展至 45+

## [2.2.3] — 2026-04-22

### Added
- Phase 2: 消息去重（dedup cache + nonce 管理）
- Phase 2: 记忆溯源（source_agent_id / source_task_id）
- 客户端 SSE 去重（event_id 递增）
- 看门狗定时清理（Dedup TTL）

### Fixed
- SSE 断线重连时的消息补发问题

## [2.2.2] — 2026-04-18

### Added
- 初始发布：消息通信 + 任务调度 + SSE 推送
- SQLite WAL 持久化
- 3 个单元测试（security / utils / dedup）
- Docker 镜像
- GitHub Actions CI/CD
