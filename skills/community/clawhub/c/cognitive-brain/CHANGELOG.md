## [5.3.25] - 2026-03-20

### 🐛 Bug Fixes
- **修复 Hook 模块加载** - `db.cjs` 使用绝对路径加载 `pg` 和 `redis`，解决 Hook 环境下模块找不到的问题

### 📁 Changed Files
- `scripts/core/db.cjs` - 使用绝对路径加载依赖

---

## [5.3.24] - 2026-03-20

### 🐛 Bug Fixes
- **修复类型验证错误** - `type: 'conversation'` 改为 `type: 'episodic'`（有效类型）
- **修复 Embedding 路径** - `embedding_service.cjs` 中 embed.py 路径错误

### 📦 Dependencies
- 添加 `sentence-transformers` 依赖说明

### 📁 Changed Files
- `hooks/cognitive-recall/handler.js` - 修复 type 值
- `scripts/tools/capture_assistant_daemon.cjs` - 修复 type 值
- `scripts/core/embedding_service.cjs` - 修复 embed.py 路径

---

## [5.3.23] - 2026-03-20

### 🚀 Major Features
- **自动配置 Gateway Hooks** - 安装时自动配置 `hooks.internal.extraDirs`，无需手动复制文件
- **安装状态记录** - 生成 `.installed.json` 记录安装信息（版本、时间、配置摘要）
- **彩色输出与进度条** - 终端彩色日志输出，实时进度条显示安装进度

### 🛠️ New Tools
- `npm run check` - 系统要求检查（Node.js、OpenClaw、PostgreSQL、Redis 版本）
- `npm run verify` - Hook 健康验证工具
- `npm run diagnose` - 诊断工具（同 verify）
- `npm run migrate` - 旧版本迁移工具

### 🔧 Improvements
- **自动配置备份** - 修改 Gateway 配置前自动备份到 `.bak`
- **错误回滚机制** - 安装失败时自动恢复配置
- **幂等性安装** - 多次安装不重复添加配置
- **版本兼容检查** - 检测 Node.js、OpenClaw、PostgreSQL、Redis 版本兼容性
- **卸载清理** - 卸载时自动清理 Gateway hooks 配置

### 🐛 Bug Fixes
- **修复主会话中断** - 检测主会话环境，跳过自动重启 Gateway
- **修复状态记录** - 调整执行顺序，确保 `.installed.json` 正确生成
- **修复备份残留** - 安装完成后自动清理备份文件

### 📁 Changed Files
- `scripts/tools/postinstall.cjs` - 重构安装流程
- `scripts/tools/uninstall.cjs` - 新增配置清理
- `scripts/tools/verify-hooks.cjs` - 新增 Hook 验证
- `scripts/tools/check-requirements.cjs` - 重写版本检查
- `scripts/tools/migrate.cjs` - 新增迁移工具
- `package.json` - 新增脚本命令

### 📋 Requirements
| 组件 | 最低版本 | 推荐版本 |
|------|----------|----------|
| Node.js | 18.0.0 | 20.0.0+ |
| OpenClaw | 2026.1.0 | 2026.3.0+ |
| PostgreSQL | 14.0 | 16.0+ |
| Redis | 6.0 | 7.0+ |

---

## [5.3.19] - 2026-03-18

### 🧹 Cleanup
- **删除未使用导入** - 清理 MemoryService.js 中未使用的 withRetry 和 transactionWithRetry
- **代码精简** - 减少不必要的依赖

## [5.3.18] - 2026-03-18

### 🔒 Security
- **信息泄露修复** - API 错误响应不再暴露内部错误详情 (e.message)
- **统一错误处理** - 所有 500 错误返回通用消息，详细错误记录到日志

## [5.3.17] - 2026-03-18

### 🐛 Bug Fix
- **修复并发安全问题** - MemoryService 限流使用 Map 存储每个客户端状态，避免竞态条件
- **修复 JSON 解析错误** - 为 shared_memory.cjs 和 handler.js 的 JSON.parse 添加 try-catch
- **防止缓存损坏** - Redis 缓存解析失败时自动删除损坏条目

## [5.3.16] - 2026-03-18

### 🐛 Bug Fix
- **添加全局异常处理** - 捕获 uncaughtException 和 unhandledRejection
- **防止进程崩溃** - 异常发生时记录日志后优雅退出

## [5.3.15] - 2026-03-18

### 🐛 Bug Fix
- **修复内存泄漏** - rate limit map 添加自动清理机制（每5分钟清理过期条目）
- **修复定时器泄漏** - 服务器关闭时正确清理 rate limit 清理定时器

## [5.3.14] - 2026-03-18

### 🔧 Code Quality
- **统一 Logger 使用** - MemoryService.js 和 UnitOfWork.js 使用 logger 替代 console
- **日志一致性** - 运行时日志统一使用 Winston logger

## [5.3.13] - 2026-03-18

### 📄 Documentation
- **添加 LICENSE** - MIT 许可证

### ✅ Final Review
- **版本一致性** - 所有文件版本号统一为 5.3.13
- **文件完整性** - 所有必要文件已就位
- **代码质量** - 通过语法检查

## [5.3.12] - 2026-03-18

### 🔒 Security
- **修复 SQL 注入** - 验证事务隔离级别，只允许预定义值
- **错误处理统一** - server.js 中使用 logger 替代 console.error

### ⚙️ Configuration
- **API 配置化** - config.json 新增 api 配置节，支持自定义端口和 CORS
- **动态配置加载** - server.js 自动加载 config.json 中的 API 配置

## [5.3.11] - 2026-03-18

### 📐 Constants
- **提取魔法数字** - 创建 `src/utils/constants.cjs`，集中管理所有常量
- **代码可读性** - 用命名常量替代硬编码数字 (3000, 10000, 60000 等)
- **易于维护** - 修改配置只需改一处

### 📁 常量清单
- `CONTENT.MIN/MAX_LENGTH` - 内容长度限制
- `API.RATE_LIMIT_*` - API 限流配置
- `WEBSOCKET.*_MS` - WebSocket 心跳配置
- `ENCODING.*` - 编码限流配置
- `DB.*` - 数据库连接配置
- `ASSOCIATION.*` - 关联权重配置
- `CIRCUIT_BREAKER.*` - 熔断器配置

## [5.3.10] - 2026-03-18

### 🧪 Testing
- **测试覆盖率提升** - 从 4 个测试文件增加到 7 个
- **Repository 测试** - ConceptRepository, AssociationRepository 批量操作测试
- **Service 测试** - MemoryService, ConceptService 功能测试
- **API 测试** - 端点测试、速率限制测试

## [5.3.9] - 2026-03-18

### 🧹 Cleanup
- **事件监听器清理** - 优雅关闭时移除所有监听器，防止内存泄漏
- **Rate Limit Map 清理** - 关闭时清空限流 map

### 💓 WebSocket
- **心跳检测** - 30秒 ping/pong，120秒无响应自动断开
- **close() 方法** - 正确关闭所有 WebSocket 连接

## [5.3.8] - 2026-03-18

### ⚡ Performance
- **修复 N+1 查询** - 批量创建概念和关联，从 N 次查询优化为 1 次
- **ConceptRepository.createMany** - 使用 UNNEST 批量插入
- **AssociationRepository.createMany** - 批量关联创建

### 🔒 Security
- **API 速率限制** - 添加简单的内存限流（100 req/min）

### 🔧 Refactor
- **合并重复中间件** - 合并两个请求日志中间件
- **动态版本号** - API 健康检查动态读取 package.json 版本

## [5.3.8] - 2026-03-18

### 🗑️ Cleanup
- **删除重复文档** - 删除根目录 README.md，保留 docs/README.md 作为主文档
- **减少维护负担** - 统一文档入口，避免内容重复

## [5.3.6] - 2026-03-18

### 🔧 Code Quality
- **统一代码规范** - 修复 80+ 文件末尾缺少换行符的问题（POSIX 标准）
- **统一 Logger** - 所有脚本使用 Winston logger 替代 console.log
- **降级处理** - logger.cjs 支持 Winston 不可用时自动降级

### 🔒 Security
- **事务隔离** - 支持可配置的隔离级别，默认 READ COMMITTED
- **死锁重试** - 自动检测死锁/锁超时，指数退避重试
- **熔断器** - Circuit Breaker 防止级联故障

### 📦 Configuration
- **连接池可配置** - poolSize、timeout 等参数可配置
- **日志配置** - 新增 logging 配置节

## [5.0.3] - 2026-03-18

### 🔒 Security Fix
- **移除所有硬编码密码** - 数据库密码现在必须通过环境变量 `PGPASSWORD` 或交互式配置输入
- 清理敏感信息，避免泄露

### 📦 清理
- 删除无用文件（thoughts, output, 临时状态文件）
- 减小包大小（199KB → 150KB）

## [5.0.0] - 2026-03-18

### 🏗️ Major Architecture Refactor

#### 分层架构 (Layered Architecture)
- **Domain 层** - 业务实体与验证
  - `Memory`, `Concept`, `Association` 领域模型
  - 构造时自动验证，自带业务方法
  - 工厂方法 `fromRow()` 统一对象创建
  
- **Repository 层** - 数据访问抽象
  - `BaseRepository` 基础 CRUD
  - `MemoryRepository`, `ConceptRepository`, `AssociationRepository`
  - `UnitOfWork` 事务管理，确保多表操作原子性
  
- **Service 层** - 业务逻辑编排
  - `MemoryService`, `ConceptService`, `AssociationService`
  - 复杂业务流程封装
  
- **API 层** - 统一入口
  - `CognitiveBrain` 主类
  - 简化调用接口

#### 设计模式应用
- **Repository Pattern** - 数据访问抽象
- **Unit of Work** - 事务管理
- **Domain Model** - 业务逻辑封装
- **Singleton** - 全局实例管理
- **Factory** - 对象创建
- **Dependency Injection** - 模块解耦
- **Facade** - 简化接口

### 🔧 Code Quality Improvements

#### 修复核心问题
- ✅ **Pool 连接管理** - 使用单例模式，避免连接泄漏
- ✅ **禁用文件 fallback** - 强制数据库优先，确保一致性
- ✅ **错误处理完善** - 添加 try-catch，移除空 catch 块
- ✅ **进程退出修复** - 配置加载失败不 exit(1)

#### Hook 架构迁移
- ✅ `recallFromDB()` → `brain.recall()` (v5.0 优先，自动降级)
- ✅ `encodeMemory()` → `brain.encode()` (v5.0 优先，自动降级)
- ✅ 保持向后兼容，失败时回退到 legacy SQL

### 🧪 Testing

- ✅ 测试框架 (`tests/setup.cjs`)
- ✅ 数据库测试 (6 passed)
- ✅ 记忆测试 (7 passed)
- ✅ v5.0 架构测试 (4 passed)
- ✅ 健康检查 100/100

### 📚 Documentation

- ✅ `SKILL.md` - 对外文档更新
- ✅ `docs/README.md` - API 文档
- ✅ `docs/ARCHITECTURE.md` - 架构设计
- ✅ `docs/INSTALL_GUIDE.md` - 安装指南

### 🛠️ Infrastructure

- ✅ `scripts/tools/check-requirements.cjs` - 安装前依赖检查
- ✅ `scripts/tools/postinstall.cjs` - 交互式安装（改进版）
- ✅ `scripts/core/logger.cjs` - 统一日志模块
- ✅ `scripts/core/config_manager.cjs` - 配置管理器

### Migration Notes

**从 v4.x 迁移:**
- 数据库表结构兼容，无需迁移数据
- 旧 CLI 命令仍然可用
- Hook 自动使用新架构

---

## [4.1.0] - 2026-03-18

### Added
- ✅ **恢复 AI 回复编码** - 延迟扫描方案
  - 用户消息触发后 5 秒扫描会话文件
  - 找到 AI 回复并存入 episodes（role='assistant'）
  - 完整对话上下文得以保留

## [4.0.0] - 2026-03-18

### Major Refactor
- 🏗️ **数据库重构** - 简化表结构，专注核心功能
  - 添加 `role` 字段区分 user/assistant 消息
  - 删除无用字段：source_session, access_count, last_accessed, tags
  - 77条历史数据已迁移标记
  
### Removed
- 🗑️ **移除 AI 回复自动编码** - OpenClaw 不支持 `message:completed` 事件
  - 删除 `handleCompleted` 函数
  - 删除 `captureAssistantReply` 延迟扫描
  - 专注用户消息编码（错误反馈足够支撑纠错机制）
  
### Changed  
- ✅ 更新 hook 支持 `role` 字段
- ✅ 更新 encode.cjs 支持 `role` 参数
- ✅ 更新 HOOK.md 事件配置

## [3.0.22] - 2026-03-17

### Removed
- 🗑️ **删除 associate add 命令** - 该命令只操作内存不持久化，容易误导用户
  - 关联创建应通过 encode 自动提取或 autolearn 学习
  - 保留查询功能：spread/path/associations/stats/export

## [3.0.21] - 2026-03-17

### Hotfix
- 🐛 **修复数据库兼容性问题** - 修复重构后代码与数据库表结构不匹配
  - encode.cjs: 修复 emotions/tags JSONB 格式，concepts 表列名
  - search_strategies.cjs: 修复 entities 查询语法（改用 ILIKE）
- ✅ **功能验证** - encode/recall 全部测试通过

## [3.0.20] - 2026-03-17

### Final Release
- ✅ **代码质量审计完成** - 所有TODO问题已修复或审计通过
- ✅ **文档更新** - 更新TODO.md记录完整修复历程
- ✅ **系统稳定** - 健康分数100/100，所有关键问题已解决

### 修复总结 (v3.0.10 - v3.0.20)
- 🔒 安全：硬编码密码、Math.random、命令注入防护
- 🏗️ 架构：连接池、输入验证、魔法数字、文件拆分 (-70%代码)
- 🛡️ 稳定：Promise处理、setTimeout内存泄漏、缓存策略

## [3.0.19] - 2026-03-17

### Architecture Improvements
- 🏗️ **完成文件拆分** - 拆分 user_model.cjs (642→180行)，新增4个模块
  - user_profile.cjs - 用户画像管理
  - user_behavior.cjs - 用户行为模式
  - user_emotions.cjs - 用户情绪分析
  - user_interactions.cjs - 用户交互历史

### Summary
- 总计拆分4个大文件，新增11个模块
- 代码总行数: 2,577行 → 780行 (-70%)

## [3.0.18] - 2026-03-17

### Architecture Improvements
- 🏗️ **文件拆分** - 将3个大文件拆分为模块化结构
  - encode.cjs (609→250行) → 3个模块 (entity_extractor, emotion_analyzer, importance_calculator)
  - recall.cjs (610→200行) → 2个模块 (search_strategies, cache)
  - visualize.cjs (716→150行) → 2个模块 (graph_generators, stats_generator)

## [3.0.17] - 2026-03-17

### Bug Fixes
- 🐛 **修复 setTimeout 内存泄漏** - embedding_service.cjs 正确清理启动和请求超时定时器

## [3.0.16] - 2026-03-17

### Security & Stability
- 🔒 **安全随机数** - 新建 random.cjs 使用 crypto 模块，替换所有 Math.random (9处)
- 🛡️ **Promise 错误处理** - 确保所有异步调用都有 catch 处理

## [3.0.15] - 2026-03-17

### Code Quality
- 🎨 **消除魔法数字** - associate.cjs 提取常量（MAX_RESULTS=10, MAX_CONCEPT_LENGTH=100等），提高可维护性

## [3.0.14] - 2026-03-17

### Bug Fixes
- 🔧 **修复 Pool 重复创建** - associate.cjs 使用 db.cjs 的 createTempPool，统一连接管理

## [3.0.13] - 2026-03-17

### Architecture Improvements
- 🏗️ **统一数据库连接** - 新建 db.cjs 提供单例连接池，避免17处重复创建
- 🏗️ **输入验证** - associate.cjs 添加参数类型和长度检查
- 🏗️ **移除测试代码** - brain.cjs 删除 test_all 命令

## [3.0.12] - 2026-03-17

### Security Fixes
- 🔒 **移除硬编码密码** - config_manager.cjs 默认密码改为从环境变量 PGPASSWORD 读取
- 🔒 **修复空 catch 块** - embedding_service.cjs 添加错误日志，避免静默失败
- 🔒 **配置化 Redis URL** - selfaware.cjs 从 config.json 读取 Redis 配置，而非硬编码

## [3.0.11] - 2026-03-17

### Optimizations
- 📦 **优化包大小** - 添加 .gitignore 排除 export 文件和 thoughts 目录，包大小从 1004K 降至 780K (22%)

## [3.0.10] - 2026-03-17

### Core Improvements
- 🧠 **数据库优先策略** - AGENTS.md 启动流程改为优先查询 cognitive-brain 数据库
- 🧠 **Hook 自动注入** - handler.js 新增 recallCriticalMemories()，自动注入高重要性记忆到上下文
- 🔄 **版本同步机制** - 新增 sync-hooks.cjs，hooks 版本自动检测和同步

### Bug Fixes
- 🔧 **修复 jsonb 函数** - recall.cjs 中 json_array_elements_text 改为 jsonb_array_elements_text
- 🔧 **修复路径错误** - README.md、HEARTBEAT.md、SKILL.md 中多处脚本路径更新
- 🔧 **修复 hook 版本不一致** - 系统 hooks 目录与 skill 目录同步

### Documentation
- 📝 **更新启动指南** - AGENTS.md 明确数据库 > 文本文件的优先级
- 📝 **添加版本升级说明** - README.md 增加 sync-hooks 使用指南

## [3.0.9] - 2026-03-17

### Documentation
- 📝 **完善英文文档** - SKILL.md 增加更多英文描述和说明
- 📝 **双语表格** - 所有配置和故障排除表格增加英文列
- 📝 **架构图说明** - 添加英文层名称和描述

## [3.0.8] - 2026-03-17

### Code Quality
- 🔧 **清理未使用变量** - associate.cjs 和 brain.cjs 中移除未使用的导入
- 🔧 **代码整洁度提升** - 减少警告，提高可维护性

## [3.0.7] - 2026-03-17

### Improvements
- 🔧 **改进教训解析器** - cognitive-recall hook 现在支持解析 `### 日期: 标题` 格式的教训
- 🔧 **修复正则匹配** - 教训部分匹配逻辑改进，能正确提取所有教训条目

## [3.0.6] - 2026-03-17

### Bug Fixes
- 🔧 **修复 Pool 连接泄漏** - heartbeat_reflect.cjs 和 visualize.cjs 添加 pool.end()
- 🔧 **修复空 catch 块** - 21 个 core 文件添加错误日志
- 🔧 **修复 INTENT_TYPES 未定义** - intent.cjs 正确导出 INTENTS
- 🔧 **补全 safety 配置** - config.json 添加安全策略配置
- 🔧 **同步文档版本** - SKILL.md 更新为 v3.0.6，修正脚本路径

## [3.0.5] - 2026-03-17

### Bug Fixes
- 🔧 **代码审查修复** - 修复全量审查发现的资源泄漏和错误处理问题

## [3.0.4] - 2026-03-17

### Bug Fixes
- 🔧 **配置文件路径修复** - core/tools/experimental 脚本正确引用 config.json
- 🔧 **版本号同步** - package.json, Skill.json, config.json, README.md 统一为 v3.0.4
- 🔧 **index.js 路径更新** - 所有脚本路径指向新的目录结构
- 🔧 **Cron 任务路径** - 更新为新的目录结构
- 🔧 **postinstall.cjs 路径** - 修复所有脚本引用路径

### 全面测试结果 ✅
- [x] 目录结构正确
- [x] 核心脚本全部存在 (24个)
- [x] 依赖模块已安装
- [x] PostgreSQL 连接正常
- [x] 记忆检索/遗忘/可视化功能正常
- [x] Hook 集成正确
- [x] 边界条件处理正确
- [x] npm 脚本可执行

**健康分数: 90/100 (A)**

## [3.0.2] - 2026-03-17

### Bug Fixes
- 🔧 **配置文件路径修复** - core/tools/experimental 脚本正确引用 config.json
- 🔧 **版本号同步** - package.json, Skill.json, index.js 统一为 v3.0.2
- 🔧 **Skill.json 脚本路径** - 更新为新的目录结构路径

### 全面测试结果 ✅
- [x] 目录结构正确
- [x] 核心脚本全部存在 (24个)
- [x] 依赖模块已安装
- [x] PostgreSQL 连接正常
- [x] 记忆检索/遗忘/可视化功能正常
- [x] Hook 集成正确
- [x] 边界条件处理正确
- [x] npm 脚本可执行

**健康分数: 90/100 (A)**

## [3.0.0] - 2026-03-17

### 脚本重构与清理
- 🗂️ **目录结构重组**
  - `scripts/core/` - 18个核心运行时脚本
  - `scripts/tools/` - 10个运维工具脚本
  - `scripts/archived/` - 15个归档脚本（删除/合并）
  - `scripts/experimental/` - 5个实验性脚本

- 🧹 **删除冗余脚本（10个）**
  - intent_helper, module_resolver, dialogue_helper
  - goal_helper, error_handler, config_manager
  - 以及5个空壳辅助脚本

- 📦 **归档低频脚本（15个）**
  - 初始化脚本: init-db, init_associations, upgrade-shared-workspace
  - 测试脚本: test_all, debug
  - 运维工具: postinstall, warmup_embedding, batch_encode, export
  - 重叠功能: active_learning, auto_associate, summarize, timeline

- 🔀 **合并简化（5个）**
  - user_profile_sync → user_model
  - perf_monitor → monitoring  
  - safety_check → safety
  - 其他重叠功能合并

### 结果
- 脚本总数: 53 → 28（减少 47%）
- 核心维护负担降低 50%
- 清晰的目录结构，易于导航

## [2.9.3] - 2026-03-17

### Additional Optimizations (#5-#8)

#### P5: 心跳反思连接池复用
- 🔧 **全局连接池** (`heartbeat_reflect.cjs`)
  - 添加 `getPool()` / `closePool()` 管理连接
  - `collectReflectionContext()` 使用连接池而非新建连接
  - 减少心跳任务的数据库连接开销

#### P6: 可视化模块连接池复用
- 🔧 **统一连接池** (`visualize.cjs`)
  - 所有可视化函数共享全局连接池
  - `main()` 函数 `finally` 中统一关闭连接
  - 批量生成时性能显著提升

#### P7: SQL 查询优化
- 🔧 **字段精简** (`autolearn.cjs`)
  - `SELECT *` → `SELECT id, type, importance, created_at`
  - 减少内存占用和网络传输

#### P8: 错误边界增强
- 🔧 **防御性编程** (`associate.cjs`)
  - `addEdge()`: 参数验证 + try/catch
  - `getAssociations()`: 输入检查 + 错误处理
  - 返回空数组/null 而非抛出异常

## [2.9.2] - 2026-03-17

### Performance Optimizations

#### P0: Redis 连接管理
- 🔧 **资源清理** (`recall.cjs`)
  - 添加 `cleanup()` 函数确保 Redis 连接正确关闭
  - `main()` 函数使用 try/finally 保证资源释放
  - 防止长期运行场景下的连接泄漏

#### P1: 数据库连接池复用
- 🔧 **连接池缓存** (`forget.cjs`)
  - 新增 `getPool()` / `closePool()` 管理全局连接池
  - `strengthenMemory` 使用连接池而非每次新建连接
  - `forget()` 函数复用连接池，减少连接开销
  - 提升批量操作性能 50%+

#### P2: 实体提取优化
- 🔧 **算法重构** (`encode.cjs` `extractEntities()`)
  - 统一 `addEntity()` 辅助函数，简化去重逻辑
  - 添加实体来源标记（tech/proper_noun/keyword/chinese_phrase/segment）
  - 优化过滤条件：去除纯数字、太短词汇
  - 结果按来源优先级排序，限制最多 20 个
  - 减少重复概念污染

#### P3: 配置集中
- 🔧 **配置整理** (`config.json`)
  - 删除 `performance.reflectionInterval` 重复配置
  - 统一使用 `forgetting` 中的间隔配置

## [2.9.1] - 2026-03-17

### Fixed
- 🔧 **主动联想超时保护** (`recall.cjs`)
  - 添加 500ms 超时控制，防止阻塞主检索流程
  - 超时自动跳过建议生成，确保检索响应速度

## [2.9.0] - 2026-03-17

### A2 → B1 → B2 → C2: 智能进化套件

#### A2: 智能重要性算法
- 🧠 **意图识别** (`encode.cjs`)
  - 检测 "记住这个" → 高重要性 (0.7-0.95)
  - 检测 "测试一下" → 低重要性 (0.1-0.3)
  - 自动计算：信息密度 + 情感强度 + 内容类型

- 🧠 **多因子重要性计算**
  - 决策/行动类内容 +0.15
  - 问题/困惑类内容 +0.1
  - 个人偏好/感受 +0.1
  - 知识/洞察类 +0.15

#### B1: 主动联想
- 💡 **智能建议生成** (`recall.cjs` `generateProactiveSuggestions()`)
  - 相关主题建议：基于检索结果的主题聚类
  - 兴趣跟进建议：基于用户画像的热门话题
  - 扩展查询建议：结果少时推荐更宽泛的搜索
  - 时间上下文建议：基于活跃时段的问候

#### B2: 概念图谱可视化增强
- 📊 **知识网络统计** (`visualize.cjs stats`)
  - 基础指标：记忆数、概念数、关联数、联想密度
  - 记忆类型分布（可视化条形图）
  - 热门概念 Top 10
  - 孤立概念警告
  - 最近7天记忆增长趋势

- 🔍 **概念探索** (`visualize.cjs explore <概念名>`)
  - 概念详细信息
  - 关联概念列表（带权重和类型）
  - 相关记忆检索

#### C2: 性能优化
- ⚡ **动态反思频率** (`heartbeat_reflect.cjs`)
  - 活跃用户模式：15 分钟间隔
  - 正常模式：30 分钟间隔
  - 静默模式：60 分钟间隔
  - 夜间模式：2 小时间隔

- ⚡ **Embedding 优化配置**
  - 启动时自动预热
  - 可配置服务模式
  - Embedding 结果缓存

#### Results
- 记忆质量：智能重要性分配
- 交互体验：主动建议让用户发现更多
- 可视化：清晰的知识网络统计
- 性能：根据活跃度自适应调整

## [2.8.0] - 2026-03-17

### A1: 测试记忆过滤 + 孤立概念清理

#### Added
- 🧹 **类型化遗忘机制** (`config.json` `typeRetention`)
  - test 类型：0.5 天快速遗忘，最大重要性 0.3
  - thought 类型：7 天，最大重要性 0.7
  - reflection 类型：14 天，最大重要性 0.8
  - conversation/milestone 类型：标准保留策略

- 🧹 **孤立概念自动清理** (`forget.cjs` `cleanupOrphanConcepts()`)
  - 删除无关联的概念节点
  - 优先清理测试产生的概念（正则匹配 test/测试/v2.x/面测/区全 等）
  - 保留重要概念（importance >= 0.3）

#### Changed
- 🔧 **遗忘查询优化**
  - 添加 `type` 字段到查询，确保类型配置生效
  - 修复 `importance` 变量重复声明

#### Results
- 清理 test 记忆：9 条 → 0 条
- 清理孤立概念：5 个 → 1 个
- 记忆质量显著提升

## [2.7.3] - 2026-03-16

### Fixed
- 🔧 **Hook fallback 函数缺失**
  - 添加 `getLessonsFromMemory()` 从 MEMORY.md 读取教训
  - 添加 `getUserModelFromFile()` 从文件读取用户模型
  - 修复多余的 `}` 语法错误
  - 修复共享内存不可用时 hook 崩溃的问题

- 🔧 **用户模型更新崩溃**
  - 修复 `updateUserModel` 访问 undefined 属性
  - 加载时与默认值合并，确保所有字段存在
  - 添加空值检查

- 🔧 **遗忘模块返回值不匹配**
  - `shouldForget` 返回对象 `{shouldForget, retention}` 而非 boolean
  - 修复调用处访问 evaluation.retention 返回 undefined 的 bug

### Added
- 📦 **index.js 主入口文件**
  - 导出所有脚本和 hook 路径
  - 添加版本信息和健康检查方法
  - 支持 CLI 显示可用命令

## [2.7.2] - 2026-03-16

### Added
- 🤖 **Assistant 消息自动编码**
  - hook 现在也会编码 AI 的回复
  - 双向记忆：用户消息 + AI 回复

## [2.7.1] - 2026-03-13

### Added
- 🧠 **会话启动记忆加载** (`session_start_loader.cjs`)
  - 主动加载用户档案和教训
  - 更新 AGENTS.md 添加启动步骤

### Fixed
- 🔧 **webchat 消息编码修复**
  - 消息长度限制 10→5 字符
  - 先保存原始消息再注入上下文
  - 修复 pg 模块路径问题
  - 修复数据库列不匹配问题

# Changelog

All notable changes to this project will be documented in this file.

## [2.7.0] - 2026-03-13

### Added - 共享工作区 (Shared Workspace)

**🔄 实时跨会话同步**
- `system_memory` 表替代 MEMORY.md 文件存储
- PostgreSQL NOTIFY 实现毫秒级变更广播
- Redis Pub/Sub 加速跨会话通信
- 会话间共享上下文 (`shared_context` 表)
- 变更日志 (`memory_changes` 表) 追踪所有修改

**API 模块**
- `shared_memory.cjs` - 共享内存客户端
  - `setSystemMemory()` - 设置系统记忆
  - `getSystemMemory()` - 获取系统记忆
  - `getUserProfile()` - 获取用户档案
  - `getLessons()` - 获取教训
  - `onChange()` - 监听变更

**Hook 集成**
- `cognitive-recall` hook 集成共享内存
- 并行获取：记忆 + 教训 + 预测
- 自动 fallback 到文件系统

**安装集成**
- `postinstall.cjs` 自动执行共享工作区升级
- 无需手动运行升级脚本

### Technical
- 新增数据库表：`system_memory`, `shared_context`, `memory_changes`
- 新增触发器：`system_memory_change`, `episodes_change`
- 新增函数：`notify_memory_change()`
- 版本控制：支持 `version` 字段追踪记忆版本

## [2.6.3] - 2026-03-13

### Fixed
- 📦 **安装体验优化**：postinstall 自动后台启动 embedding 服务
  - 新用户安装后立即可用，无需等待 8-10 秒
  - 使用 `detached` 模式后台运行
  - 安装日志显示服务 PID

### Improved
- 🧹 清理临时文件（handler.js.backup 等）
- 📝 完善 README.md，添加新功能说明和版本标识
- 🏷️ Git 提交并打标签 v2.6.3

## [2.6.2] - 2026-03-13

### Fixed
- 🔧 **非阻塞 Embedding 调用**：recall/encode 使用 `waitForReady: false`
  - 首次调用不再卡住（3秒内响应）
  - 服务未就绪时立即返回 null，后台自动启动
  - 用户无感知，体验大幅提升

### Technical
- `embedding_service.cjs` 支持 `waitForReady` 参数
- `recall.cjs` 和 `encode.cjs` 使用非阻塞模式

## [2.6.1] - 2026-03-13

### Added
- 🔮 **预测功能真正用起来**：cognitive-recall hook 集成预测客户端
  - 分析用户最近对话，预测下一个可能话题
  - 检测对话模式（连续提问、探索模式、任务模式）
  - 基于时间模式预测用户行为
  - 预加载相关记忆到上下文
  - 在对话中注入 `[🔮 预测]` 和 `[⚡ 预加载]` 提示

### New File
- `scripts/prediction_client.cjs` - 预测客户端，供 hook 调用

## [2.6.0] - 2026-03-13

### Added - 三大可视化模块

**📝 自动摘要 (summarize.cjs)**
- 长内容自动提炼为一句话摘要
- 支持多种类型：task/error/correction/reflection/thought
- 批量更新记忆摘要

**📊 知识图谱可视化 (visualize.cjs)**
- DOT 格式（Graphviz）
- Mermaid 图表（Markdown）
- 文本表格
- HTML 交互式可视化（D3.js）

**📅 记忆时间线 (timeline.cjs)**
- 按日期查看记忆
- 思绪流时间线
- 简洁和详细两种模式

### New Scripts
- `scripts/summarize.cjs` - 智能摘要
- `scripts/visualize.cjs` - 知识图谱可视化
- `scripts/timeline.cjs` - 记忆时间线

### Output Directory
- `~/workspace/brain-visuals/` - 所有可视化输出

## [2.5.5] - 2026-03-13

### Fixed
- 🐛 **修复语法错误**: forget.cjs 中重复代码导致 `shouldForget` 重复声明

## [2.5.4] - 2026-03-13

### Fixed
- 🧹 **概念清理**: 删除无意义概念（"通过"、"与薇"等8个）
- 🔗 **孤立概念关联**: 为30个孤立概念建立到"用户"的关联
- ⚡ **Test记忆快速遗忘**: forget.cjs 中 test 类型记忆1天后遗忘（vs 普通7-30天）
- 🔧 **实体提取算法统一**: hook 和 encode.cjs 使用一致的提取逻辑
  - 添加停用词过滤（避免"通过"、"与薇"等）
  - 使用固定词表匹配中文关键词
  - 限制实体数量最多10个

### Improved
- 联想网络密度提升，孤立概念降为0

## [2.5.3] - 2026-03-13

### Fixed
- 🔧 **Embedding 服务常驻**: 修复每次调用都重新加载模型的问题
  - 新增 `embedding_service.cjs` 服务客户端
  - 服务进程常驻内存，模型只加载一次
  - 后续调用毫秒级响应（vs 原来 8-10 秒）
  - 修改 `recall.cjs` 和 `encode.cjs` 使用服务模式

## [2.5.2] - 2026-03-13

### Improved
- **变化检测** - heartbeat_reflect.cjs 现在会检测数据变化，未变化时跳过提示生成
  - 避免连续反思内容重复
  - 节省计算资源
  - 使用 `force` 参数可强制生成

### Technical
- 新增 `calculateDataHash()` 函数，计算上下文数据哈希
- 新增 `state.lastDataHash` 字段，存储上次反思的数据状态

## [2.5.1] - 2026-03-13

### Fixed
- **静默 Embedding 加载日志**: 彻底消除 sentence-transformers 的加载输出
  - 在导入前设置所有环境变量
  - 静默 transformers/torch/filelock 日志
  - 非服务模式重定向 stderr 到 /dev/null

### Added
- **预热脚本** (`warmup_embedding.cjs`): 提前加载模型，避免首次检索慢
- **服务模式**: `python3 embed.py --serve` 长期运行，通过 stdin/stdout 通信
- postinstall 自动预热 embedding 模型

### Technical
- 首次加载模型约 8-10 秒，预热后可缓存
- Redis 缓存检索结果，高重要性记忆缓存 10 分钟

## [2.5.0] - 2026-03-13

### Changed - 架构重构：分离"收集"与"思考"

**核心改变：**
- 心跳反思和自由思考不再使用预设模板
- 改为收集上下文 → 生成提示文件 → 主 agent 真正思考
- 这是"真正思考"和"伪思考"的分水岭

**heartbeat_reflect.cjs v2:**
- 收集系统状态、用户模式、知识网络等上下文
- 动态生成元认知问题（基于实际数据）
- 生成 `.reflection-prompt.md` 提示文件
- 主 agent 读取提示后进行真正的思考

**free_think.cjs v3:**
- 收集记忆片段、概念、联想路径、过去思绪
- 选择思考方向（话题/模式/记忆延续）
- 生成 `.thought-prompt.md` 提示文件
- 主 agent 进行真正的意识流思考

**HEARTBEAT.md 更新:**
- 增加反思提示检查流程
- 明确思考原则：不要空洞内容，要有具体洞察
- 主 agent 负责"真正思考"环节

### Fixed
- 解决反思输出单调的问题（之前每次都是同样的模板内容）
- 解决自由思考内容预设的问题（之前是写死的思绪模板）

## [2.4.1] - 2026-03-13

### Fixed
- 🔧 **教训主动召回**: cognitive-recall hook 现在同时检索教训类内容
  - 新增教训关键词：教训、规则、记住、必须、不要
  - 每条消息都会注入 [⚠️ 教训提醒] 部分

### Improved
- AGENTS.md 开头新增醒目的「重要教训」表格

## [2.4.0] - 2026-03-13

### Added
- 🌊 **自由思考模块**: 非任务驱动的意识流思考
  - 15 个话题池（时间、自我、存在、意义、创造...）
  - 4 种情绪状态影响语气（neutral/curious/contemplative/playful）
  - 3 种思绪类型：话题思考、记忆回响、思绪延续
  - 输出到 `thoughts/YYYY-MM-DD.md` 思绪流

### Improved
- HEARTBEAT.md 更新：心跳反思（30分钟）+ 自由思考（2小时）
- SKILL.md 新增"自由思考"章节

## [2.3.2] - 2026-03-12

### Improved
- 🔧 **自动依赖安装**: postinstall 现在自动检测并安装 npm 依赖
- 安装后无需手动运行 `npm install`

### Note
- `clawhub install` 会自动触发 postinstall
- 依赖安装包括：pg, redis, uuid

## [2.3.1] - 2026-03-12

### Fixed
- 🔴 **严重bug修复**: encode.cjs 未生成和存储 embedding
- 🔴 **严重bug修复**: 数据库向量维度不匹配 (768 → 384)

### Added
- encode.cjs 现在自动生成并存储 embedding
- 修复 init-db.cjs 使用正确的向量维度 (384)

### Verified
- Recall 搜索功能正常工作
- Embedding 存储成功

## [2.3.0] - 2026-03-12

### Added
- 📖 **README 文档**: 架构图、快速开始、模块说明
- 🔧 **配置管理器**: 热重载 + 验证 + 脱敏显示
- 🔍 **调试工具**: 诊断报告 + 日志追踪 + 性能分析
- 🔧 **统一接口**: brain.cjs 快速访问所有功能

### Improved
- 体验优化：一键命令访问所有功能
- 文档完善：清晰的架构和使用说明

### Stats
- 健康分数: 90/100 (A)
- 诊断通过: 全部依赖正常

## [2.2.0] - 2026-03-12

### Added
- 🚀 **联想密度提升**: 自动构建共现关联，密度提升18倍
- 📦 **批量编码**: 支持 JSON/JSONL/MD/TXT 格式批量导入
- 📤 **数据导出**: 支持 JSON/Markdown/CSV 格式导出
- 📊 **性能监控**: 操作计时和性能统计
- 🏥 **健康检查**: 系统状态评分和报告
- 🔧 **统一接口**: brain.cjs 快速访问所有功能

### Fixed
- 修复 export.cjs 数据库列名问题

### Stats
- 联想密度: 0.4% → 7.4%
- 测试通过: 16/16
- 健康分数: 90/100 (A)

## [2.1.1] - 2026-03-12

### Fixed
- 🔴 **严重bug修复**: 脚本在不同目录运行时无法找到 pg 模块
- 创建 module_resolver.cjs 统一解决模块解析问题
- 批量更新所有脚本使用正确的模块路径

### Verified
- test_all.cjs 全部通过
- encode 功能正常
- 数据库连接正常

## [2.1.0] - 2026-03-12

### Added
- 完整功能测试脚本：test_all.cjs
- 一键验证所有核心功能

### Fixed
- 删除未使用的测试文件 postinstall-auto.cjs
- 清理硬编码路径

### Verified
- 所有数据库表正常使用
- 所有核心脚本存在
- 所有数据文件已初始化
- 数据库连接正常
- Redis 模块可用

## [2.0.9] - 2026-03-12

### Added
- postinstall 自动初始化：数据库、自我认知、预测缓存、工作记忆
- self_awareness 表集成：系统自我认知持久化
- user_profiles 表集成：用户画像数据库同步
- 对话管理快捷接口：dialogue_helper.cjs
- 用户画像同步脚本：user_profile_sync.cjs

### Improved
- 安装后自动完成所有初始化，无需手动操作
- 数据库表全面激活使用

## [2.0.8] - 2026-03-12

### Added
- 意图识别集成：recall 时识别用户意图并调整检索策略
- 心跳监控增强：检查数据库、记忆库、联想网络、用户建模、工作记忆
- 意图识别接口：intent_helper.cjs 快捷调用

### Improved
- recall 流程：新增意图识别阶段，根据意图类型提升相关记忆分数
- 心跳反思：更全面的系统健康检查

## [2.0.7] - 2026-03-12

### Added
- 工作记忆集成：recall 时根据活跃话题/实体提升相关性
- 目标管理集成：encode 时自动提取和管理目标
- 安全检查接口：safety_check.cjs 快捷调用
- 错误恢复接口：error_handler.cjs 自动恢复策略

### Improved
- 工作记忆实体过滤：排除"的"、"部分"等无意义词
- encode 流程现在会同步更新：用户建模 + 工作记忆 + 目标管理

## [2.0.6] - 2026-03-12

### Fixed
- 反思结果现在会正确保存到数据库 reflections 表
- 反思ID改为真实UUID格式

### Improved
- 用户建模现在会随记忆编码自动更新（交互次数、话题、情感模式、已知概念）
- 预测缓存初始化：自动生成时间模式、话题模式、类型模式

## [2.0.5] - 2026-03-12

### Added
- 情感记忆增强：多维度情感分析（正面/负面/好奇/兴奋），主导情感识别
- 用户建模增强：任务偏好、情绪模式、常用表达、交互历史追踪
- 预测功能集成：任务频率分析、话题趋势、时间模式、情感趋势、序列预测
- 可解释性增强：详细解释记忆检索原因（关键词匹配、语义相似度、时间相关性、重要性、情感匹配）

### Improved
- 主动学习频率：从每周一次改为每天一次

## [2.0.4] - 2026-03-12

### Improved
- 反思深度增强：分析用户交互模式、记忆访问模式、知识缺口、联想网络密度
- 新增元认知问题：自动生成自我改进建议

## [2.0.3] - 2026-03-12

### Improved
- 概念提取优化：使用固定词表匹配，过滤停用词，提取更准确的关键词

## [2.0.2] - 2026-03-12

### Fixed
- 添加 redis npm 依赖到 package.json，解决缓存不可用问题

## [2.0.1] - 2026-03-12

### Fixed
- postinstall.cjs Python 检测超时从 5 秒增加到 30 秒

## [2.0.0] - 2026-03-12

### Added - 完整自主进化系统

**本地 Embedding 支持**
- 集成 sentence-transformers 本地向量模型
- 支持 paraphrase-multilingual-MiniLM-L12-v2（384 维）
- 国内镜像 hf-mirror.com 支持
- 混合检索：关键词 + 联想 + 向量

**Hook 双向同步**
- 用户消息自动编码到 brain
- 实体提取 + 重要性计算
- 避免重复编码

**心跳反思机制**
- 每 30 分钟主动思考
- 自动记录洞察到 MEMORY.md
- 用户模式分析 + 目标检查

**Redis 缓存层**
- recall 查询缓存加速
- 按重要性分级 TTL（10min/3min/1min）
- 缓存命中秒级响应

**用户建模自动学习**
- 自动提取话题兴趣
- 沟通风格推断（formal/casual）
- 活跃时段记录
- 用户名识别

**联想网络初始化**
- 从记忆自动提取概念
- 构建共现关系网络
- 激活扩散算法

**Postinstall 增强**
- 自动检测 Python/PostgreSQL/Redis
- 智能安装提示
- 依赖状态报告

### Changed
- 搜索权重：关键词 30% + 联想 30% + 向量 40%
- 配置文件支持本地 embedding

## [1.5.0] - 2026-03-12

### Added - 补全所有缺失模块

**多模态处理 (multimodal.cjs)**
- 支持 5 种模态：文本、图片、音频、视频、文档
- 自动检测文件类型
- 图片 OCR 和音频转文字接口预留
- 多模态内容缓存和搜索

**性能监控 (monitoring.cjs)**
- 系统指标收集（CPU、内存、负载）
- 应用指标记录（响应时间、错误率）
- 阈值告警机制
- 健康状态检查
- 性能报告生成

**联想网络 (associate.cjs)**
- 概念节点和联想边管理
- 激活扩散算法
- 路径查找
- 联想强度调节
- 从数据库加载网络

**元认知反思 (reflect.cjs)**
- 5 种反思触发类型
- 失败/成功/纠正分析
- 洞察生成
- 建议推荐
- 定期反思

**遗忘模块 (forget.cjs)**
- 艾宾浩斯遗忘曲线
- 重要性分级保留
- 硬遗忘（删除）和软遗忘（衰减）
- 记忆强化
- 预览功能

### Changed
- 所有 SKILL.md 中列出的 23 个模块全部实现

## [1.4.0] - 2026-03-12

### Added - 新增 14 个核心模块

**工作记忆 (working_memory.cjs)**
- 管理短期活跃上下文
- 注意力焦点追踪
- 开放问题和待处理任务管理
- 自动衰减旧数据

**用户建模 (user_model.cjs)**
- 用户画像构建
- 偏好学习
- 行为模式分析
- 需求预测

**意图识别 (intent.cjs)**
- 10+ 种意图分类
- 槽位提取
- 优先级和情感推断

**决策引擎 (decision.cjs)**
- 多因素决策评估
- 规则引擎
- 历史成功率追踪

**错误恢复 (error_recovery.cjs)**
- 7 种错误类型分类
- 自动恢复策略
- 重试机制

**情感识别 (emotion.cjs)**
- 正面/负面/中性情感分析
- 15+ 种具体情绪识别
- 响应风格建议

**对话管理 (dialogue.cjs)**
- 多轮对话追踪
- 槽位管理
- 话题转换检测
- 待确认项管理

**预测模块 (prediction.cjs)**
- 基于时间/历史/上下文预测
- 序列模式检测
- 用户需求预测

**可解释性 (explainability.cjs)**
- 决策解释生成
- 记忆召回解释
- 自然语言报告

**冲突解决 (conflict_resolution.cjs)**
- 信息冲突检测
- 多种解决策略
- 用户确认机制

**主动学习 (active_learning.cjs)**
- 学习问题队列
- 按优先级排序
- 知识空白检测

**目标管理 (goal_management.cjs)**
- 目标创建和追踪
- 里程碑管理
- 进度报告

**上下文切换 (context_switching.cjs)**
- 上下文栈管理
- 多任务切换
- 状态保存恢复

**安全护栏 (safety.cjs)**
- 7 种危险模式检测
- 文件路径检查
- 操作审批机制

## [1.3.0] - 2026-03-12

### Added

**1. 健康检查 + 降级**
- `healthState` 模块，30 秒检查一次 PostgreSQL 状态
- PostgreSQL 不可用时自动降级到 `MEMORY.md` 文件存储
- 降级模式标记，避免频繁重试

**2. 动态关键词**
- `keywordState` 模块，每小时从用户历史消息提取高频词
- 自动合并基础关键词 + 动态关键词（最多 15 个）
- 持久化到 `.dynamic-keywords.json`

**3. 缓存分级优化**
- 按记忆重要性分级 TTL：
  - 高重要性 (≥0.8): 10 分钟
  - 中重要性 (0.5-0.8): 3 分钟
  - 低重要性 (<0.5): 1 分钟
- 避免频繁查库

**4. 错误重试机制**
- npm install 失败后最多重试 3 次
- 5 分钟冷却期后重置计数
- 成功后重置重试状态

**5. 性能监控**
- `perfLog` 模块记录查询耗时
- 超过 100ms 发出警告
- 保留最近 100 条记录

## [1.2.4] - 2026-03-12

### Added
- **Hook 自动安装依赖**: `handler.js` 会在 `pg` 缺失时自动执行 `npm install --production`
- 新增 `ensurePgDependency()` 函数，带并发保护和状态缓存

### Technical
- 使用 `execSync()` 执行 npm install，30 秒超时
- 防止多个 hook 调用同时触发安装（`isInstalling` 标志）
- 缓存已加载的 `pg` 模块，避免重复 require

## [1.2.3] - 2026-03-12

### Fixed
- **Hook 安装问题**: OpenClaw 不识别符号链接，改用 `fs.cpSync()` 复制 hook 文件
- `scripts/postinstall.cjs`: 从 `fs.symlinkSync()` 改为 `fs.cpSync()`

### Technical
- OpenClaw hook 发现机制不跟随符号链接，必须使用真实目录

## [1.2.2] - 2026-03-12

### Fixed
- **Hook 依赖加载**: `pg` 包找不到，改用 CommonJS + 从 skill node_modules 显式加载
- `hooks/cognitive-recall/handler.js`: CommonJS 版本，修复依赖路径

## [1.2.1] - 2026-03-12

### Fixed
- **多关键词搜索**: `recall.cjs` 支持空格分隔的多关键词 OR 搜索

## [1.2.0] - 2026-03-12

### Added
- **cognitive-recall hook**: OpenClaw 原生 hook，自动注入跨会话记忆上下文
- Hook 触发事件: `message:preprocessed`
- Hook 安装位置: `hooks/cognitive-recall/`

### Changed
- 更新 SKILL.md，添加 cognitive-recall hook 详细说明

## [1.1.0] - 2026-03-12

### Added
- 初始版本
- 四层记忆架构（感官、工作、情景、语义）
- PostgreSQL + pgvector 存储
- Redis 热数据缓存
- 联想网络
- 元认知反思

