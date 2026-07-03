# 技术栈分级选择指南

本文件帮助 AI 工具根据用户的构建规模选择合适的技术库。

---

## Python 生态

### 日志 (Logging)

| 级别 | 推荐 | 替代 | 说明 |
|---|---|---|---|
| **Minimal** | `print()` | — | 零依赖，适合脚本级项目 |
| **Professional** | `structlog` | `loguru` | 结构化日志，支持上下文绑定 |
| **Enterprise** | `structlog` + OpenTelemetry | `loguru` + otel | 全链路追踪，日志关联 trace_id |

选择依据：
- Minimal：代码量 < 500 行，仅需基础调试输出
- Professional：需要 JSON 格式日志输出到文件或日志收集器
- Enterprise：多服务/多 Agent 协同，需要关联追踪和集中日志平台

### CLI (命令行接口)

| 级别 | 推荐 | 替代 | 说明 |
|---|---|---|---|
| **Minimal** | `input()` + `argparse` | — | 标准库，无需安装 |
| **Professional** | `click` | `typer` | 装饰器风格，自动生成 help |
| **Enterprise** | `typer` + `rich` | `click` + `rich` | 类型安全 + 美化 TUI 输出 |

选择依据：
- Minimal：单命令脚本，参数 ≤ 3 个
- Professional：多子命令，需要 `--help` 自动生成
- Enterprise：复杂 CLI Tree，需要进度条/表格/颜色输出

### HTTP Client

| 级别 | 推荐 | 替代 | 说明 |
|---|---|---|---|
| **Minimal** | `urllib` (标准库) | — | 基本 HTTP 请求 |
| **Professional** | `httpx` (async) | `aiohttp` | 异步优先，HTTP/2 支持 |
| **Enterprise** | `httpx` + 连接池 | `aiohttp` | 连接复用，超时重试策略 |

选择依据：
- Minimal：单次 API 调用，无需异步
- Professional：并发请求，需要 async/await
- Enterprise：高并发，需要连接池管理和熔断器

### Schema / Validation (数据验证)

| 级别 | 推荐 | 替代 | 说明 |
|---|---|---|---|
| **Minimal** | 无 | — | 手动类型检查 |
| **Professional** | `dataclasses` | `attrs` | 类型注解，零依赖 |
| **Enterprise** | `pydantic` v2 | `msgspec` | 运行时验证 + JSON Schema 导出 |

选择依据：
- Minimal：简单数据结构，字段 ≤ 5 个
- Professional：嵌套对象，需要类型安全
- Enterprise：API 契约验证，需要序列化/反序列化保证

### Testing (测试)

| 级别 | 推荐 | 替代 | 说明 |
|---|---|---|---|
| **Minimal** | 无 | — | 手动测试或 `assert` |
| **Professional** | `pytest` + `pytest-asyncio` | `unittest` | fixture + mock 支持 |
| **Enterprise** | `pytest` + `coverage` + `tox`/`nox` | — | CI/CD 集成，多 Python 版本矩阵 |

选择依据：
- Minimal：探索性代码，无持续维护需求
- Professional：需要回归测试，异步代码覆盖
- Enterprise：多环境矩阵测试，覆盖率门禁 (≥ 80%)

### 沙箱 (Sandbox)

| 级别 | 推荐 | 替代 | 说明 |
|---|---|---|---|
| **Minimal** | 路径白名单 | — | 纯 Python 实现，~50 行 |
| **Professional** | `docker-py` | subprocess + Docker | 容器隔离，~200 行 |
| **Enterprise** | Firecracker SDK | gVisor runtime | 微 VM 隔离，~500 行 |

选择依据：
- Minimal：信任级别高，仅需文件路径保护
- Professional：需要进程级隔离，多租户场景
- Enterprise：零信任环境，需要内核级隔离和凭证外置

### 监控 (Monitoring)

| 级别 | 推荐 | 替代 | 说明 |
|---|---|---|---|
| **Minimal** | 无 | — | — |
| **Professional** | `prometheus-client` | 自定义 metrics | 指标导出到 `/metrics` |
| **Enterprise** | OpenTelemetry + Prometheus + Grafana | Datadog | 全链路可观测 |

选择依据：
- Minimal：个人使用，无监控需求
- Professional：需要基础指标（请求量/延迟/错误率）
- Enterprise：需要告警规则、Dashboard、Trace 关联

### 配置管理 (Configuration)

| 级别 | 推荐 | 替代 | 说明 |
|---|---|---|---|
| **Minimal** | `python-dotenv` | `os.environ` | `.env` 文件加载 |
| **Professional** | `PyYAML` + `pydantic-settings` | — | YAML 配置 + 类型验证 |
| **Enterprise** | `pydantic-settings` + 7 级层级覆盖 | — | 多源合并 (默认 < 文件 < 环境变量 < 命令行 < 远程) |

选择依据：
- Minimal：配置项 ≤ 5 个，仅需环境变量
- Professional：多环境配置 (dev/staging/prod)，YAML 管理
- Enterprise：配置中心集成，动态热更新

### 数据库 (可选，用于记忆/日志持久化)

| 级别 | 推荐 | 替代 | 说明 |
|---|---|---|---|
| **Minimal** | 无 | — | 文件系统存储 (JSON/JSONL) |
| **Professional** | SQLite (`aiosqlite`) | — | 嵌入式，无需运维 |
| **Enterprise** | PostgreSQL (`asyncpg`) | CockroachDB | 生产级，支持连接池和副本 |

选择依据：
- Minimal：无持久化需求或文件即够用
- Professional：需要 SQL 查询能力，单机部署
- Enterprise：需要高可用、备份恢复、水平扩展

---

## Node.js / TypeScript 生态

### 日志 (Logging)

| 级别 | 推荐 | 替代 | 说明 |
|---|---|---|---|
| **Minimal** | `console.log()` | — | 内建 API |
| **Professional** | `pino` | `winston` | 高性能 JSON 日志 |
| **Enterprise** | `pino` + OpenTelemetry | `winston` + otel | 分布式追踪集成 |

### CLI

| 级别 | 推荐 | 替代 | 说明 |
|---|---|---|---|
| **Minimal** | `process.argv` | — | 手动解析 |
| **Professional** | `commander` | `yargs` | 声明式命令定义 |
| **Enterprise** | `oclif` + `ink` | `commander` + `chalk` | 框架级 CLI + React TUI |

### HTTP Client

| 级别 | 推荐 | 替代 | 说明 |
|---|---|---|---|
| **Minimal** | `fetch` (内建) | — | Node 18+ 原生支持 |
| **Professional** | `undici` | `axios` | 高性能 HTTP 客户端 |
| **Enterprise** | `undici` + 连接池 | `got` | 连接复用 + 重试策略 |

### Schema / Validation

| 级别 | 推荐 | 替代 | 说明 |
|---|---|---|---|
| **Minimal** | 无 | — | TypeScript 类型注解 |
| **Professional** | `zod` | `yup` | 运行时验证 + 类型推导 |
| **Enterprise** | `zod` + `typebox` | `io-ts` | JSON Schema 生成 |

### Testing

| 级别 | 推荐 | 替代 | 说明 |
|---|---|---|---|
| **Minimal** | 无 | — | 手动测试 |
| **Professional** | `vitest` | `jest` | 快速 ESM 优先 |
| **Enterprise** | `vitest` + `playwright` + CI matrix | `jest` + `puppeteer` | E2E + 多 Node 版本 |

### 沙箱 (Sandbox)

| 级别 | 推荐 | 替代 | 说明 |
|---|---|---|---|
| **Minimal** | `vm2` (已弃用) / 路径白名单 | — | 需注意安全性 |
| **Professional** | `isolated-vm` | `dockerode` | V8 隔离 + Docker |
| **Enterprise** | `isolated-vm` + Firecracker | `dockerode` + gVisor | 多级隔离 |

### 监控 (Monitoring)

| 级别 | 推荐 | 替代 | 说明 |
|---|---|---|---|
| **Minimal** | 无 | — | — |
| **Professional** | `prom-client` | 自定义 | Prometheus 指标 |
| **Enterprise** | OpenTelemetry JS SDK + Grafana | Datadog | 全链路 |

### 配置管理

| 级别 | 推荐 | 替代 | 说明 |
|---|---|---|---|
| **Minimal** | `dotenv` | `process.env` | `.env` 加载 |
| **Professional** | `convict` | `config` | Schema 验证 |
| **Enterprise** | `convict` + 远程配置源 | `node-config` | 多源合并 |

### 数据库 (可选)

| 级别 | 推荐 | 替代 | 说明 |
|---|---|---|---|
| **Minimal** | 无 | — | 文件系统 |
| **Professional** | SQLite (`better-sqlite3`) | — | 同步高性能 |
| **Enterprise** | PostgreSQL (`pg` / `drizzle-orm`) | — | 生产级 |

---

## 决策规则 (Decision Rules)

构建 Agent 时，按以下优先级规则选择技术栈：

### 规则 1：规模优先原则
```
Minimal       → 标准库优先，0-2 个三方依赖，所有功能在单文件内
Professional  → 选择成熟稳定的库，5-8 个依赖，模块化组织
Enterprise    → 全套生态栈，10+ 个依赖，需考虑可观测性和运维
```

### 规则 2：一致性原则
- 同一项目中，所有模块应遵循同一级别
- 不允许 `Minimal` 级别的日志 + `Enterprise` 级别的验证混合
- 升级路径：应从 Minimal 平滑迁移到 Professional，不得跳级

### 规则 3：可替换原则
- 每个推荐都有一个备选方案
- 备选应在功能上等价，仅在实现风格上不同
- 当推荐库出现重大 Breaking Change 时，可快速切换到替代

### 规则 4：依赖收敛原则
- Professional 级别总依赖数应控制在 8 个以内
- Enterprise 级别总依赖数应控制在 20 个以内（含传递依赖优化）
- 每个依赖的选择需有明确理由（性能/生态/维护性）

---

## 反模式 (Anti-Patterns)

| 反模式 | 后果 | 正确做法 |
|---|---|---|
| Minimal 规模引入 `pydantic` | 过度工程，依赖膨胀 | 使用 `dataclasses` 或手动验证 |
| Professional 规模使用 `print()` | 缺乏结构化日志，调试困难 | 使用 `structlog` / `pino` |
| Enterprise 规模缺少 OpenTelemetry | 不可运维，故障定位困难 | 集成 OTel SDK |
| 跨层混用 (Mixed Tiers) | 代码风格不一致，维护成本高 | 统一技术栈层级 |
| 选择已弃用的库 | 安全漏洞，无上游支持 | 检查库的维护状态和社区活跃度 |
| 仅凭流行度选择 | 不符合实际需求 | 按决策规则评估匹配度 |
| 忽略生态兼容性 | 依赖冲突 (Diamond Dependency) | 检查传递依赖的版本约束 |

---

⚠ **AI 构建提示**：

```
当用户选择构建规模后，你应：

1. 识别规模标签 (Minimal / Professional / Enterprise)
2. 遍历上表中该规模对应的推荐项
3. 将推荐依赖写入 pyproject.toml 或 package.json
4. 仅在选择 Enterprise 时引入 OpenTelemetry 相关依赖
5. 仅在选择 Professional+ 时引入测试框架
6. 确保不引入属于更高规模层级的依赖（如 Minimal 不得有 pydantic）

检查清单：
□ 日志库与规模匹配
□ CLI 库与规模匹配
□ 验证库与规模匹配
□ 测试框架未在 Minimal 中引入
□ Enterprise 级别包含监控依赖
□ 所有推荐使用其最新稳定版本
```