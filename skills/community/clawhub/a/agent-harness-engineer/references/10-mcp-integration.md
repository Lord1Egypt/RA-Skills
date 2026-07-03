# MCP 集成

## 协议概述

MCP（Model Context Protocol）定义了 AI 模型与外部工具、数据源之间的标准化接口。在 Harness 架构中，MCP 是 Agent 扩展能力的主要入口——通过 MCP Server 注册的工具和资源，Agent 可以获得超出内置工具的领域特定能力。

**核心概念：**
- **Server**：提供工具和数据的服务端（独立进程或远程服务）
- **Client**：使用工具和数据的客户端（即 Agent Harness）
- **Tool**：Agent 可以调用的功能（参数化操作）
- **Resource**：Agent 可以访问的数据（文件、数据库、API 结果等）
- **Transport**：Client 与 Server 之间的通信管道

---

## 六种传输协议选择指南

每种传输协议有不同的适用边界。选错协议会导致性能问题或架构耦合：

### stdio（标准输入输出）

**工作原理**：Client 通过子进程的 stdin/stdout 与 MCP Server 通信。Server 作为 Client 的子进程启动。

**何时选择：**
- 本地工具（文件系统操作、本地数据库查询、代码分析工具）
- 零配置要求——不需要网络、不需要认证
- 天然进程隔离：Server 崩溃不影响 Client

**何时避免：**
- 需要跨机器访问（stdio 绑死在同一台机器）
- Server 需要保持长时间运行的状态（随 Client 进程生命同期）
- 需要负载均衡（一个 Server 只能服务一个 Client）

**启动参数模式**：通过命令 + 参数指定 Server 可执行文件路径，环境变量注入配置。

### HTTP + SSE（Server-Sent Events）

**工作原理**：HTTP 承载请求，SSE 承载 Server 到 Client 的推送（如资源变更通知）。这是远程 MCP 的标准选择。

**何时选择：**
- 远程服务（跨网络 / 跨数据中心）
- 需要负载均衡（多个 Client 共享同一个 Server 集群）
- Server 需要独立部署和运维（不随 Client 生命周期绑定）
- 需要 Server 主动推送事件（资源更新、告警）

**何时避免：**
- 本地场景：HTTP 引入不必要的网络栈复杂度和延迟
- 对延迟极度敏感（~1ms 级别）：HTTP 的 TCP 握手和 Header 开销不可忽略

**关键设计要点**：HTTP 端点接收请求并返回初始响应，SSE 长连接保持打开用于推送后续更新。

### WebSocket

**工作原理**：全双工持久连接，Client 和 Server 可以在任意时刻主动发送消息。

**何时选择：**
- 实时交互场景（如协作编辑、实时监控面板）
- 需要双向高频率推送（Client 和 Server 都需要主动发送）
- SSE 的"Server → Client 单向流"不够用

**何时避免：**
- 简单的请求-响应模式：WebSocket 的连接管理开销超过 HTTP
- Server 不需要主动推送的任何场景

### gRPC

**工作原理**：基于 HTTP/2 + Protocol Buffers 的高性能 RPC 框架，支持双向流。

**何时选择：**
- 高性能微服务（需要毫秒级延迟和protobuf 零拷贝序列化）
- 已有 gRPC 基础设施的组织（服务网格、统一的 proto 定义）
- 需要类型安全的接口契约（proto 文件即契约）

**何时避免：**
- 协议要求简单的场景：gRPC 需要 proto 编译步骤和 stubs 生成，增加构建复杂度
- 浏览器环境：gRPC-web 可用但功能受限
- 对外提供给第三方：REST API 的通用性远高于 gRPC

### Local（同进程函数调用）

**工作原理**：工具直接作为内存中的函数注册，无序列化、无进程边界。

**何时选择：**
- 极低延迟需求（函数调用 < 1μs）
- 工具逻辑简单且可信（不需要安全隔离）
- 原型阶段（快速集成，跳过 MCP Server 开发）

**何时避免：**
- 需要安全隔离：同进程内无隔离，工具崩溃可能导致 Agent 进程崩溃
- 需要语言无关性：Local 模式绑死 Agent 实现语言
- 工具逻辑复杂或需要独立资源管理

### 协议选型决策树

```
需要跨机器访问？
  ├── 是 → 需要实时双向通信？
  │         ├── 是 → WebSocket
  │         └── 否 → 需要 protobuf 契约？
  │                   ├── 是 → gRPC
  │                   └── 否 → HTTP + SSE
  └── 否 → 需要安全隔离？
            ├── 是 → stdio（子进程隔离）
            └── 否 → Local（同进程函数调用）
```

---

## 连接管理（抽象设计）

### 连接池化

```
连接池策略：
  ├── 每个 MCP Server 地址维护一个连接池
  ├── 池大小：min 2, max 10（根据并发工具调用量动态伸缩）
  ├── 连接生命周期：
  │   ├── 创建：懒加载，首次调用时建立
  │   ├── 空闲回收：连接空闲 > 300s → 关闭（释放 Server 资源）
  │   └── 保活：每 60s 发送 ping（保持长连接存活）
  └── 连接分配：从池中取空闲连接 → 绑定到当前工具调用 → 调用完成后归还池
```

### 超时策略

```
多层超时体系：
  ├── 连接超时（Connect Timeout）：10s
  │   - 建立 TCP/进程连接的最大等待时间
  │   - 超时后重试 1 次（不同 IP / 重新启动子进程）
  ├── 请求超时（Request Timeout）：30s
  │   - 单次工具调用的最大等待时间（含 Server 处理时间）
  │   - 超时 → 中断当前调用 → 返回超时错误给 Agent
  └── 空闲超时（Idle Timeout）：300s
      - 连接池中空闲连接的最大保活时间
      - 超时 → 关闭连接，从池中移除
```

### 重连策略

```
指数退避重连：
  ├── 第 1 次失败：立即重试（可能有瞬时网络抖动）
  ├── 第 2 次失败：等待 1s 后重试
  ├── 第 3 次失败：等待 2s 后重试
  ├── 第 4 次失败：等待 4s 后重试
  ├── 第 5 次失败：等待 8s 后重试
  └── 第 6 次失败：标记 Server 不可用 → 通知 Agent → 停止重试

  不可重试的错误（立即停止）：
    ├── 认证失败（4xx）—— 重试无意义
    ├── 工具不存在（ToolNotFound）—— Server 配置问题
    └── 参数校验失败 —— 重新传同等参数仍然失败
```

---

## OAuth 集成（远程 MCP Server 认证）

远程 MCP Server 使用 OAuth 2.0 进行认证。集成流程通过抽象接口描述：

### 认证流程

```
抽象认证流程：
  Step 1 —— 发现（Discovery）
    Client 向 Server 的 /.well-known/oauth-authorization-server 获取 OAuth 元数据
    返回：authorization_endpoint, token_endpoint, scopes_supported

  Step 2 —— 授权（Authorization）
    用户通过浏览器访问 authorization_endpoint
    授权成功后，Server 通过 redirect_uri 返回 authorization_code
    (若为本地 Server，redirect_uri 可用 localhost 回调或设备码流程)

  Step 3 —— 换 Token（Token Exchange）
    Client 用 authorization_code + client_id + client_secret 向 token_endpoint 换取 access_token + refresh_token
    access_token 有效期通常 1 小时，refresh_token 有效期通常 30 天

  Step 4 —— 使用（Usage）
    每次工具调用时，Client 在 HTTP Header 中附带：
    Authorization: Bearer <access_token>
    或对于 stdio 传输，通过环境变量注入 token

  Step 5 —— 刷新（Refresh）
    access_token 过期 → Client 用 refresh_token 向 token_endpoint 静默刷新
    若 refresh_token 也过期 → 回退到 Step 1 重新授权
```

### 抽象接口

```
OAuthManager 抽象：
  ├── discover_auth_metadata(server_url) → OAuthMetadata
  │   - 从 Server 获取授权端点信息
  │   - 缓存元数据，避免每次重发现
  ├── initiate_authorization(metadata, scopes) → AuthRequest
  │   - 生成 authorization URL + PKCE code_verifier
  ├── exchange_code(auth_code, verifier) → TokenPair
  │   - 用 authorization_code 换取 access_token + refresh_token
  ├── refresh_access_token(refresh_token) → TokenPair
  │   - 用 refresh_token 刷新，返回新 token 对
  └── get_valid_token(server_id) → access_token
      - 检查 token 是否过期 → 过期则自动刷新
      - 返回始终有效的 access_token 或抛出 AuthError
```

**Token 安全存储：**
- Token 存储在操作系统的凭据管理器（macOS Keychain / Windows Credential Manager / Linux Secret Service）
- 不写入明文文件，不进入 Agent 的沙箱
- 每个 MCP Server 独立 token，不共享

---

## 资源生命周期

MCP 资源代表 Agent 可以读取的数据。资源管理遵循"发现 → 订阅 → 读取 → 取消订阅"的生命周期：

```
资源生命周期状态机：
                ┌──────────┐
     discover → │ UNKNOWN  │ ← 初始状态
                └────┬─────┘
                     │ subscribe
                     v
                ┌──────────┐
                │ SUBSCRIBED│ ← 已订阅，接收更新推送
                └────┬─────┘
                     │ read
                     v
                ┌──────────┐
                │  CACHED   │ ← 读取后结果缓存，减少重复请求
                └────┬─────┘
                     │ update notification (from Server via SSE/WebSocket)
                     v
                ┌──────────┐
                │  STALE    │ ← 缓存过期，下次 read 时重新请求
                └────┬─────┘
                     │ unsubscribe
                     v
                ┌──────────┐
                │ UNSUBSCRIBED│ ← 取消订阅，资源不可用
                └──────────┘

Transition triggers:
  discover → SUBSCRIBED: Agent 首次请求访问资源时自动订阅
  SUBSCRIBED → CACHED: read() 完成后缓存 TTL 内
  CACHED → STALE: Server 推送更新通知 或 TTL 过期
  STALE → CACHED: 下次 read() 时触发重新拉取
  SUBSCRIBED → UNSUBSCRIBED: 会话结束或 Agent 显式取消
```

**订阅管理抽象：**
```
ResourceManager 抽象：
  ├── discover_resources(server_id) → ResourceCatalog
  ├── subscribe(resource_uri) → Subscription
  ├── read(resource_uri) → ResourceContent
  │   - 若在 CACHED 状态且未过期 → 返回缓存
  │   - 若在 STALE 状态 → 重新拉取后更新缓存并返回
  ├── on_update(resource_uri, callback) → None
  │   - 注册回调：Server 推送更新时触发
  └── unsubscribe(subscription) → None
```

---

## 工具发现缓存策略

每次 Agent 做工具调用前，重新发现工具列表（`list_tools`）是极大的浪费——典型场景中工具列表在整个会话中不变化。

```
发现缓存三层架构：
  Level 1 —— 内存缓存（Priority: 最高, TTL: 整个会话生命周期）
    ├── 首次 list_tools 结果存入内存
    ├── 后续所有 tool_use 块从内存缓存中查找工具定义
    └── 失效条件：Server 显式发送 tool_list_changed 通知

  Level 2 —— 会话缓存（Priority: 中, TTL: 当前 Session）
    ├── 跨轮次复用：同一 Session 内不重复发现
    └── 但每次 API 调用仍需将工具定义序列化到请求体

  Level 3 —— 动态发现（Priority: 低, TTL: 无缓存）
    ├── MCP Server 启动时、连接恢复时触发
    └── 仅在收到 tool_list_changed 通知时重新拉取
```

**关键规则：**
- `list_tools` 调用不进入 Agent 的 token 计费（Harness 层开销）
- 工具定义注入到 LLM 请求时受 Prompt Cache 前缀稳定性策略控制
- MCP 工具追加在稳定前缀之后，不破坏缓存

---

## 错误处理策略

```


### 指数退避 + 电路断路器

```
指数退避重试（Exponential Backoff）：

  重试序列：第 1 次 → 立即 | 第 2 次 → 1s | 第 3 次 → 2s | 第 4 次 → 4s
  最大重试次数：5
  最大等待时间：30s
  抖动因子：±25%（避免惊群效应）

  不可重试错误（立即放弃）：
    ├── ToolNotFound — 工具名称拼写错误或 Server 不支持
    ├── InvalidParams — 参数类型/格式错误
    ├── AuthError — Token 过期或无效
    └── PermissionDenied — 无权限执行

电路断路器（Circuit Breaker）：

  三个状态：
  ┌──────────┐  失败 > N 次  ┌──────────┐  冷却时间到期  ┌─────────────┐
  │  CLOSED  │ ─────────────→ │   OPEN   │ ─────────────→ │ HALF_OPEN   │
  │ (正常)   │                │ (熔断)   │                │ (试探恢复)   │
  └──────────┘                └──────────┘                └──────┬──────┘
       ↑                          ↑                            │
       │                          │                    成功 ← 试探请求
       │                          │                            │
       │                          │                    失败 ──→ 回到 OPEN
       └──────────────────────────┘
          失败计数重置（时间窗口滑动）

  参数：
    ├── 失败阈值（failureThreshold）：滑动窗口内 5 次失败 → 触发 OPEN
    ├── 冷却时间（cooldownPeriod）：30s 内保持 OPEN 状态
    ├── 试探请求数（halfOpenMaxRequests）：HALF_OPEN 状态最多允许 3 次试探
    └── 滑动窗口（windowSize）：60s 内累计失败数
```

**错误传播到 Agent：**
```
Harness 层错误 → Agent 层信息转换：

MCP 层错误              → Agent 可见信息
────────────────────────────────────────────
连接超时                → "工具 X 当前不可用：Server 未响应"
电路断路器熔断          → "工具 X 暂时被禁用：Server 近期多次失败，将在 30s 后自动重试"
ToolNotFound            → "工具 X 不存在：请检查工具名称和 Server 配置"
AuthError               → "工具 X 认证失败：请重新连接 MCP Server"
InvalidParams           → "工具 X 参数错误：{具体字段}格式不正确"
StaleCache              → "工具 X 返回了过期缓存结果：正在重新获取最新数据"
```

---

## 规模适应性指南

### Minimal（最小可行）

- 仅支持 stdio 传输（本地工具，零配置）
- 无连接池（每次调用启动子进程，用完销毁）
- 无 OAuth（所有 Server 在本地，不需要远程认证）
- 无资源订阅（仅支持工具的请求-响应模式）
- 简单重试：3 次固定间隔重试，无电路断路器
- 代码量：~200 行（直接调用 MCP SDK）

### Professional（专业级）

- stdio + HTTP/SSE 双协议支持
- 连接池：min 2, max 5
- 资源生命周期：discover → subscribe → read（无自动更新推送）
- 工具发现缓存：Level 1 内存缓存（会话级）
- OAuth：支持 Authorization Code 流程
- 指数退避重试：5 次，最大 30s
- 代码量：~600-1000 行

### Enterprise（企业级）

- 全部 6 种传输协议可选
- 连接池：动态伸缩，基于负载自适应
- 电路断路器：完整三状态实现
- 资源生命周期完整 + Server 推送实时更新
- 工具发现缓存：三层架构 + `tool_list_changed` 通知自动失效
- OAuth：Authorization Code + PKCE + Token 自动刷新 + 凭据管理器存储
- 监控埋点：每 Server 的 QPS、P50/P99 延迟、错误率、缓存命中率
- 多区域支持：Server 就近路由（按 Client 地理位置选择最近的 Server 节点）
- 代码量：~1500-2500 行

---

## AI 构建提示

构建 MCP 集成层时，AI 不应直接复制代码，而应根据以下提示自行实现：

1. **传输层抽象**：先建 `Transport` 抽象接口——`connect()`, `send(message)`, `receive() → message`, `close()`。所有 6 种传输协议实现此接口。上层 `MCPClient` 只依赖 `Transport`，不感知底层协议。

2. **工具发现缓存**：使用 TTL Cache 模式。`list_tools` 结果缓存到内存，key = server_id，过期后自动重新拉取。Server 推送 `notifications/tools/list_changed` 时强制失效。

3. **OAuth 流程**：不要硬编码 client_id 和 client_secret。通过环境变量或操作系统凭据管理器注入。Token 刷新在后台自动执行，请求线程不感知。

4. **资源订阅**：使用观察者模式。`ResourceManager` 内部维护 `uri → Set<callback>` 的映射表。Server 推送更新时遍历回调列表通知所有订阅方。

5. **连接池**：使用对象池模式。不要自己从零实现池——若语言有成熟连接池库（如 Python 的 `aiopg`、TypeScript 的 `generic-pool`），优先复用而非自建。

6. **错误分类**：将 MCP 协议错误码映射到内部错误类型（NetworkError, AuthError, ToolError, ResourceError）。映射表可配置，方便扩展新错误码。

7. **测试策略**：
   - 单元测试：token 刷新逻辑（模拟过期）→ 验证自动刷新；连接池分配和归还 → 验证无泄漏
   - 集成测试：启动真实 MCP Server（stdio）→ 调用 list_tools → 调用每个工具 → 验证结果
   - 混沌测试：随机断开 Server 连接 → 验证重连和电路断路器行为

8. **监控埋点**：每个 `call_tool` 操作记录开始时间、结束时间、Server ID、工具名、结果状态（success/error/timeout）。这些指标用于电路断路器的决策和运维面板。