# API/接口/胶水公约在插件语境的映射（CLAUDE.md 蒸馏）

> 工作区 `CLAUDE.md` 是"API/接口/胶水全链路公约"，但其面向 HTTP/REST 与 IDL 项目。
> 本文给出它到 Cordis 插件开发的**可用性映射**：哪些直接用、哪些转译、哪些不适用，
> 以及插件语境专属的契约规范。写插件时按此对齐，别照搬 REST 条款也别漏掉转译。

## 三层结论（先记住这个）

```
CLAUDE.md 三大部分 → 插件语境
│
├─ 第 0 章 核心哲学 ──► ✅ 直接可用，强制遵守
│     契约优先 / 胶水轻薄 / 可观测 / 简单第一
│
├─ 第 3 章 胶水规范 ──► ✅ 直接可用（bridge.py 即范本）
│     职责边界 / 前置校验 / 异常翻译 / 超时熔断 / 日志
│
├─ 第 1 章 API 设计 ──► ❌ REST 专属不适用
│     少数原则转译：字段命名→snake/camel、版本→Config 演进、幂等→RPC 标注
│
└─ 第 2 章 IDL 契约 ──► 🔄 原则可用、命名转译
       ISP/类型明确/演进兼容 → 工具 JSON Schema 与 Config 设计准则
```

> 原因：Cordis 插件是**进程内服务**，没有 HTTP 门面层；"对外 API"对应的是
> 模型可见的工具契约、事件契约、Slot 协议——不是 REST 端点。

| 层级 | CLAUDE.md 条款 | 对插件 |
|---|---|---|
| 核心哲学（第 0 章）| 契约优先 / 胶水轻薄 / 可观测 / 简单第一 | ✅ **直接可用，强制遵守** |
| 胶水规范（第 3 章）| 职责边界 / 健壮性 / 可观测性 | ✅ **直接可用**（dsh-memory bridge.py 即范本） |
| API 设计（第 1 章）/ IDL（第 2 章）| URL / HTTP 方法 / 状态码 / proto / OpenAPI | ❌ 不适用；少数原则**转译**后可用 |

> 原因：Cordis 插件是**进程内服务**，没有 HTTP 门面层；"对外 API"对应的是
> 模型可见的工具契约、事件契约、Slot 协议——不是 REST 端点。

## 2. 直接可用的条款（照用）

| CLAUDE.md | 插件落地 |
|---|---|
| 契约优先：先定契约后写实现 | Config schema / 工具 JSON Schema / 事件 payload 先行 |
| 胶水轻薄：只做连接与转换 | bridge.py 薄胶水，不含业务逻辑 |
| 禁止全局状态 | 副作用全走 `ctx.on`/`ctx.effect`（traps #26） |
| 异常翻译 | 下游异常 → 统一错误（bridge `{"id","error":{code,message}}`） |
| 超时与熔断 | 跨系统调用设超时 + 指数退避重试（ChildProcessBridge 范本） |
| 前置校验 | defineTool 参数校验 + Config schema 验证 |
| 可观测 | 胶水日志 caller/callee/req/res/cost_ms |
| 职责单一（ISP） | 工具/服务拆小，不设计"上帝工具" |

## 3. 需转译的条款（改语境后用）

| CLAUDE.md | 插件语境转译 |
|---|---|
| 字段命名统一（camel/snake 禁混）| 桥接层显式 snake↔camel 转换（traps #23），禁透传裸 RPC |
| 版本兼容（增可选✅/删字段❌/改语义❌）| Config schema 演进：新增字段给 `default()`；破坏性变更升 Package 版本 |
| 幂等性声明 | 工具 `execute` / RPC 方法标注幂等性，指导重试 |
| 响应包装统一 | RPC 统一 `{"id","result"|"error"}` 包装（stdio JSON-RPC） |
| 时间格式统一 | 跨语言桥接时间字段统一 ISO 8601 或毫秒戳 |
| 契约设计原则（类型明确/演进兼容）| 工具参数 JSON Schema 与 Config schema 的设计准则 |

## 4. 不适用条款（勿照搬）

- 1.1 URL 端点设计（名词复数 / kebab-case 路径 / 查询参数）
- 1.4 HTTP 状态码双轨制
- 1.6 分页与排序标准化
- 2.1/2.2/2.4 IDL 组织与命名（proto / OpenAPI / Java）
- 第 7 章工具表（SpringDoc / gRPC / Jaeger）

> 若插件恰好封装 HTTP 服务（如 MCP 客户端），1.x 可部分回用——但那是"插件内部实现"，
> 不是插件本身的对外契约。

## 5. 插件语境专属契约（CLAUDE.md 没有，但必须守）

| 契约 | 依据 | 详情 |
|---|---|---|
| 工具契约 | `defineTool` | JSON Schema 参数 + output.render + execute；模型可见面与执行分离（[harness-integration.md](../30-capability/harness-integration.md)） |
| 事件契约 | `ctx.on` | emit/waterfall/serial/parallel 模式；waterfall 必须 `next()`（[events.md](../20-develop/events.md) / [events-catalog.md](../20-develop/events-catalog.md)） |
| Slot 协议 | `slots.register` | single/list/keyed/chain 注册协议；先查树再写（[client-ui.md](../30-capability/client-ui.md)） |
| Service 命名 | 扁平命名空间 | 加辨识前缀，避占用名（[plugin-forms.md](../00-understanding/plugin-forms.md)） |
| 版本语义 | Package 不可变 | 改代码 = 追加新 Package；current/next 指针（[dynamic-plugins.md](../30-capability/dynamic-plugins.md)） |

## 6. 逐条对照明细（CLAUDE.md 全章节）

> 判定：✅ 直接用 / 🔄 转译后用 / ❌ 不适用。构建插件时按此对齐。

### 第 0 章 核心哲学 —— 全部 ✅
| 条款 | 判定 | 落点 |
|---|---|---|
| 显式陈述假设 | ✅ | 不猜 API，先 `cordis_inspect_*` 查契约 |
| 契约优先 | ✅ | Config schema / 工具 JSON Schema 先行 |
| 胶水轻薄 | ✅ | bridge.py 只做转换转发 |
| 可观测 | ✅ | ctx.logger + 桥接日志 |
| 简单第一 | ✅ | 根治问题，不临时打补丁 |

### 第 1 章 API 设计（对外门面）
| 条款 | 判定 | 说明 |
|---|---|---|
| 1.1 URL 端点设计 | ❌ 主体 | 插件无 HTTP 门面；kebab-case → 事件命名（agent/status）已如此 |
| 1.2 HTTP 方法幂等 | 🔄 | GET/POST 幂等语义 → 工具/RPC 方法标注幂等（store 类不幂等、查询类幂等） |
| 1.3 字段命名统一 | 🔄 | TS camel ↔ Python snake 显式转换（traps #23），禁透传 |
| 1.3 统一包装层 | ✅ | RPC `{"id","result"|"error"}` 即统一包装；error 含 code+message |
| 1.3 时间格式 | ✅ | 跨语言桥接时间字段统一 ISO 8601 或毫秒戳 |
| 1.3 货币/金额 | ✅ 泛化 | 精确值不用 float——泛化为"不 lossy 类型" |
| 1.4 状态码双轨 | 🔄 | RPC 错误双轨：协议错误（JSON-RPC -32700/-32601/-32603）vs 业务错误码 |
| 1.5 版本控制 | 🔄 | URL /v1 → Package 版本；兼容规则（增可选✅/删字段❌）→ Config schema 演进 |
| 1.6 分页排序 | ❌ | 除非工具返回列表 → 转译 topK/limit 参数约定 |

### 第 2 章 接口文件契约
| 条款 | 判定 | 说明 |
|---|---|---|
| 2.1 文件组织 | 🔄 | `/api/<模块>/<版本>/` → `src/types.ts` 集中契约；同文件聚合 ✅ |
| 2.2 命名约定 | 🔄 | `XxxReq/XxxRes` → TS `*Params/*Result`；枚举 UPPER_SNAKE ✅ |
| 2.3 契约设计原则 | ✅ | ISP 职责单一、类型明确、幂等声明、演进兼容 |
| 2.4 技术栈补充 | ❌ | proto/OpenAPI/Java 无对应；"契约与实现同步"精神保留 |

### 第 3 章 胶水代码 —— 全部 ✅（核心适用区）
| 条款 | 判定 | 落点 |
|---|---|---|
| 3.1 职责边界 | ✅ | bridge 零业务逻辑；可替换性 |
| 3.2 前置校验 | ✅ | defineTool 参数校验 + Config schema |
| 3.2 禁全局状态 | ✅ | 副作用全走 ctx.effect（traps #26） |
| 3.2 异常翻译 | ✅ | 下游异常 → 统一 error 格式 |
| 3.2 超时熔断 | ✅ | ChildProcessBridge 30s 超时 + 指数退避 |
| 3.3 统一日志 | ✅ | traceId/caller/callee/req/res/cost_ms → ctx.logger |
| 3.4 跨语言实践 | 🔄 | C++↔Python → JS↔Python stdio JSON-RPC |

### 第 4/5/6/7 章
| 章节 | 判定 | 说明 |
|---|---|---|
| 4 三者边界 | ✅ | 门面=工具/服务契约、图纸=types.ts、翻译=bridge |
| 5 API 检查项 | ❌ | URL/HTTP 动词无对应 |
| 5 接口文件检查项 | ✅ | 职责单一/类型明确/演进兼容 |
| 5 胶水检查项 | ✅ | 5 项全适用 |
| 6 项目执行要点 | ✅ | 插件项目在此追加专属约束 |
| 7 工具表 | ❌ | SpringDoc/gRPC/Jaeger 是 Web 栈；转译：契约→schemastery/typert、追踪→ctx.logger |

## 7. 检查清单（胶水/契约交付前）

- [ ] 胶水层零业务逻辑；方法可替换不伤骨骼
- [ ] snake/camel 显式转换；无透传裸 RPC
- [ ] 下游异常已翻译为统一错误；含失败阶段/原文/修复建议日志
- [ ] 跨系统调用有超时 + 幂等重试
- [ ] 工具/事件/Slot 契约先查 Provider 精确契约再实现
- [ ] Config schema 演进符合版本兼容规则（增可选/不删字段）
