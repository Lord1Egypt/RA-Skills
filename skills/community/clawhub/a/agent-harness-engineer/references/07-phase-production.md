# Phase 7: 生产化

## 目标

将基础可运行的 Agent Harness 提升为可观测、可测试、可部署的生产级系统。核心不是"加测试加日志"，而是建立三层可观测架构，让系统在任意规模下都能被理解、被度量、被信任。

---

## 设计原理

Harness 架构自带一个被低估的免费特性：**Session 事件日志本身就是审计日志**。

Agent 每轮执行产生的 SessionEvent（user_input → LLM 调用 → tool 执行 → 结果 → 下一轮），其完整序列天然构成"谁在何时做了什么"的审计记录。传统系统需要额外建设审计管道，Harness 只需要持久化 SessionEvent 流即可同时获得：

- **调试能力**：回溯任意一次 Agent 执行的完整思维链
- **合规审计**：每一次外部工具的调用都有时间戳、参数、结果
- **成本归因**：每个 Session 消耗的 token 量和调用次数精确可追溯

因此，Phase 7 的架构决策应该围绕"如何让 SessionEvent 流被可靠地捕获、存储、查询、告警"展开，而非零散地添加监控点。

---

## 三层可观测架构

Claude Code 本身使用 OpenTelemetry + gRPC 进行遥测，Harness 应遵循相同模式，构建三层可观测体系：

```
┌─────────────────────────────────────────────────────┐
│                   SessionEvent 流                    │
├──────────┬──────────────────┬───────────────────────┤
│  Trace   │     Metrics       │        Logs           │
├──────────┼──────────────────┼───────────────────────┤
│ 追踪一次 │ 度量全局趋势      │ 记录结构化事件         │
│ 完整的   │ 和统计分布        │ 用于审计和问题定位     │
│ 执行链路 │                   │                       │
├──────────┼──────────────────┼───────────────────────┤
│OpenTele- │ Prometheus +      │ 结构化 JSON Logs      │
│metry +   │ Datadog           │ (Session 事件日志      │
│Langfuse  │                   │  天然是审计日志)       │
└──────────┴──────────────────┴───────────────────────┘
```

### Trace — 追踪完整执行链路

**目的**：了解一个 Agent Session 从头到尾发生了什么，哪个环节耗时最长，LLM 被调用了多少次。

- 一个 Session 对应一个 Root Span
- 每一次 LLM API 调用创建一个子 Span，携带属性：model、provider、token_count、latency_ms
- 每一次 Tool 执行创建一个子 Span，携带属性：tool_name、success、error_message
- 每一次 Compaction（上下文压缩）创建一个子 Span，标记压缩前后消息数量
- Langfuse 专门为 LLM 追踪设计，能自动捕获 prompt/completion token 消耗、流式响应的首 token 延迟、以及完整对话树

**企业级参考栈**：OpenTelemetry SDK → OTLP Collector → Langfuse Backend（LLM 专用追踪）+ Jaeger/Tempo（通用分布式追踪）

### Metrics — 度量全局趋势

**目的**：不关心某个特定 Session，而是回答"系统过去一小时平均延迟是多少""今天错误率是否飙升"。

关键指标定义：

| 指标 | 类型 | 说明 |
|------|------|------|
| `agent_session_duration_seconds` | Histogram | Session 完整执行时长分布 |
| `llm_call_latency_seconds` | Histogram | LLM 单次调用延迟（p50/p95/p99） |
| `llm_token_consumed_total` | Counter | 按 model 分组的 token 消耗总量 |
| `tool_execution_total` | Counter | 按 tool_name + status 分组的工具执行次数 |
| `tool_execution_success_rate` | Gauge | 工具执行成功率（success / total） |
| `compaction_triggered_total` | Counter | Compaction 触发次数及压缩比 |
| `session_active_count` | Gauge | 当前活跃 Session 数量 |

**企业级参考栈**：prometheus_client → Prometheus → Grafana Dashboard + AlertManager 告警规则

### Logs — 结构化事件记录

**目的**：每一个 SessionEvent 都应该以结构化 JSON 形式持久化，既是"运行日志"也是"审计日志"。

- 避开 Python 标准库 `logging` 的字符串格式化，直接使用 structlog 或 loguru 输出 JSON
- 每条日志携带固定字段：session_id、turn_number、agent_id、tenant_id（多租户场景）
- 关键事件必须记录：
  - `session.started` / `session.completed` / `session.failed`
  - `llm.call.start` / `llm.call.end`（含 token 用量）
  - `tool.exec.start` / `tool.exec.end`（含参数哈希，避免敏感数据入日志）
  - `compaction.executed`（含压缩前后统计）
- 日志级别规范：DEBUG（内部细节）/ INFO（Session 生命周期事件）/ WARNING（可恢复异常）/ ERROR（需要人工介入）

**设计要点**：SessionEvent 日志流可以双写——JSON Lines 文件（本地开发）+ 消息队列（生产环境），消费端同时写入时序数据库和对象存储。

---

## 测试策略

### 测试金字塔

```
         ╱  E2E  ╲         少量：真实 LLM + 真实工具
        ╱          ╲         验证端到端场景
       ╱ Integration ╲      中等：Mock LLM 但真实工具/Session
      ╱                ╲     验证组件协作
     ╱      Unit         ╲   大量：纯逻辑单元
    ╱──────────────────────╲  验证 Agent 循环、Token 预算、
                               Compaction 算法、工具 Schema 解析
```

**核心原则**：Agent 系统的测试难点在于 LLM 的不确定性。单元测试应该将 Agent 循环逻辑与 LLM 调用彻底解耦——通过注入确定的 LLM 响应序列，验证状态机的状态迁移是否符合预期。

### 各层测试职责

**单元测试**（数量最多，运行最快）：
- Agent 核心循环：给定 N 条预设 LLMResponse（模拟多轮对话），验证 SessionState 的 turn_count、消息列表、终止条件
- Token 预算管理：验证接近上限时的 Compaction 触发逻辑、注入空预算后的安全停止
- Compaction 算法：给定输入消息序列，验证压缩后关键信息不丢失、消息数减少
- 工具选择 (tool_choice)：验证多种 LLMResponse 格式（带 tool_calls、不带、并行调用）都能正确解析
- 错误重试策略：验证网络超时、速率限制、5xx 等场景下的重试次数和退避逻辑
- 配置解析：验证 llm_config 缺省值填充、多 provider 配置互斥检查

**集成测试**（数量中等）：
- Session 生命周期：创建 → 多轮对话 → 完成 → 验证完整 SessionEvent 流
- 工具注册与执行：注册多个工具 → 模拟带 tool_call 的 LLMResponse → 验证工具被正确调用
- Session 持久化与恢复：执行一半 → 序列化 Session → 新实例加载 → 从中断点继续
- LLM Client 适配层：使用 WireMock/响应录制，测试 Anthropic/OpenAI/本地模型三种 adapter 的正确适配

**端到端测试**（数量最少，运行最慢）：
- 只覆盖 1-2 个核心场景（如：文件读取工具 → LLM 理解内容 → 返回摘要）
- 使用真实（或测试用低成本）LLM，验证完整的 Turn → LLM → Tool → Event 链路
- 建议在 CI 中设置为可选执行（手动触发或 Nightly），避免每次 PR 都消耗 API 费用

### Mock 策略

- `LLMClient`: 核心 Mock 对象，注入预设响应序列
- `ToolExecutor`: 对真实工具做 Mock，验证参数传递和返回值处理
- `Clock/Scheduler`: Mock 时间，验证超时和重试逻辑
- **不 Mock**: TokenCounter（基于 tiktoken 的纯计算）、Event 数据结构

---

## 抽象接口层

以下是各子系统的接口抽象，不提供具体实现代码，只描述接口契约和设计意图。

### Logging 接口抽象

```
LoggingSystem
├── setup(level: str, output: LogOutput) → None
│   初始化日志系统，output 可以是 stdout / file / kafka / loki
│
├── get_logger(name: str, bindings: dict) → Logger
│   获取绑定了上下文的 Logger，bindings 预注入 session_id / agent_id 等
│   所有通过此 Logger 输出的日志自动携带绑定字段
│
└── Logger
    ├── debug(event: str, **kwargs)     → 内部状态细节
    ├── info(event: str, **kwargs)      → 生命周期事件
    ├── warning(event: str, **kwargs)   → 可恢复异常
    └── error(event: str, **kwargs)     → 需要人工介入
```

**设计要点**：
- `get_logger` 的 `bindings` 参数是关键——它让调用方在创建 logger 时一次性绑定 session_id/agent_id，后续所有日志自动携带，消除"每条日志手动传 context"的样板代码
- 输出格式应该是**结构化 JSON**，每个字段独立索引，避免字符串拼接日志
- 企业级需要支持日志级别热更新（通过配置中心下发，无需重启）

### Metrics 接口抽象

```
MetricsSystem
├── counter(name: str, labels: dict) → Counter
│   单调递增计数器，用于 token 消耗、工具调用次数、错误次数
│
├── histogram(name: str, buckets: list[float]) → Histogram
│   分布统计，用于延迟、token 数等需要分位数的指标
│
├── gauge(name: str, labels: dict) → Gauge
│   可增可减的瞬时值，用于活跃 Session 数、队列深度
│
└── Counter / Histogram / Gauge
    ├── inc(value: float = 1)          → 递增
    └── observe(value: float)           → 记录样本（仅 Histogram）
```

**设计要点**：
- Histogram 的 bucket 边界需要根据实际 LLM 延迟分布设置：建议 0.1s / 0.5s / 1s / 2s / 5s / 10s / 30s / 60s
- `tool_execution_total` 的 labels 应包括 `tool_name` 和 `status`（success / error / timeout）
- 企业级需要 Label 基数控制——tool_name 理论上无限，考虑对工具名做分桶或 top-N 截断
- 提供 `registry()` 方法输出所有已注册指标，方便 Prometheus HTTP handler 暴露 `/metrics` 端点

### Tracer 接口抽象

```
TracerSystem
├── start_span(name: str, parent: Span | None) → Span
│   创建 Span，parent 为空时以当前活跃 Span 为父
│
└── Span (context manager)
    ├── set_attribute(key: str, value: str|int|float|bool)
    │   在 Span 上设置键值属性，序列化到 Trace 后端
    │
    ├── add_event(name: str, attributes: dict)
    │   在 Span 时间线上标记一个事件点（如 "compaction.start"）
    │
    ├── set_status(status: StatusCode)
    │   标记 Span 结果：OK / ERROR
    │
    └── record_exception(exception: Exception)
        记录异常信息到 Span
```

**设计要点**：
- Span 必须是 Context Manager（`with tracer.start_span(...) as span:`），确保异常退出时也能正确 end
- 每个 Span 自动记录开始和结束时间戳
- 企业级集成 Langfuse 时，额外属性：generation_name、prompt_template_hash、input/output token 计数
- Session Span 结构：
  ```
  session.run (root)
  ├── turn.1
  │   ├── llm.call (attributes: model, provider, latency, tokens)
  │   └── tool.execute (attributes: tool_name, success, latency)
  ├── turn.2
  │   ├── llm.call
  │   ├── compaction.execute (attributes: before_count, after_count)
  │   └── llm.call (compaction 后的第二次 LLM 调用)
  └── ...
  ```

---

## AI 构建提示

当使用 AI 编码助手实现 Phase 7 时，按以下顺序给 AI 下达指令：

1. **"为 AgentCore 的 run() 方法添加 OpenTelemetry Span，每个 turn 创建一个子 Span，记录 model 和 turn_number 属性"** — 先打通 Trace 链路
2. **"创建 MetricsCollector 单例，注册 counter/histogram/gauge，并在 LLM 调用和 Tool 执行点嵌入 inc/observe 调用"** — 再嵌入 Metrics 埋点
3. **"将现有 logging.info 替换为 structlog，所有日志输出结构化 JSON，日志入口 get_logger 接受 context 字典注入 session_id"** — 最后统一日志格式
4. **"编写 AgentCore 循环的单元测试，注入 3 轮预设 LLMResponse 序列，验证最终 SessionState"** — 从核心循环开始测试
5. **"创建 conftest.py，提供 mock_llm_client fixture，返回可配置的 LLMResponse 序列"** — 建立测试基础设施
6. **"定义 Dockerfile 和 docker-compose.yaml，包含 Agent 服务 + Prometheus + Grafana"** — 建立可观测性栈

**常见 AI 构建误区**：
- 一次性要求 AI 实现全部功能 → 应分步、每次一个可验证的子目标
- 直接复制 AI 生成的测试用例不审查断言 → SessionState 的断言必须覆盖所有关键字段
- 忽略 Session Span 的层级结构 → 先画 Span 树再编码

---

## 规模适应性指南

### 最小规模（个人项目/原型）

**不需要**测试、可观测框架、部署脚本。保持轻量。

| 维度 | 做法 |
|------|------|
| 测试 | 不写测试，通过手动运行验证 |
| 日志 | `print()` 输出到控制台即可 |
| 指标 | 不采集，运行时肉眼观察 |
| Trace | 不需要 |
| 部署 | 本地 `python main.py` 运行 |
| 凭据 | `.env` 文件，`.gitignore` 排除 |
| Session 持久化 | 不需要，重启即丢弃 |

**何时升级**：当系统需要给第二个人使用时。

### 专业规模（团队工具/SaaS）

**需要**完整的测试、结构化日志、基础指标。这是最需要扎实建设的阶段。

| 维度 | 做法 |
|------|------|
| 测试 | pytest + fixtures + mocks，核心循环覆盖率 > 80% |
| 日志 | structlog 或 loguru，输出结构化 JSON 到文件 |
| 指标 | prometheus_client，暴露 `/metrics` 端点，记录 token 消耗和延迟 |
| Trace | OpenTelemetry SDK 基础 Span，本地 Jaeger 查看 |
| 部署 | Docker Compose，包含 Agent + Prometheus + Grafana |
| CI/CD | GitHub Actions / GitLab CI，PR 触发单元+集成测试 |
| 凭据 | CI/CD Secret Variables + 运行环境变量注入 |
| Session 持久化 | SQLite 单文件（适合单实例），或本地 JSON Lines 文件 |
| 告警 | Grafana Alert 规则：错误率 > 5% 或 p95 延迟 > 30s |

**关键决策点**：选择 structlog（与标准 logging 兼容，渐进式迁移）还是 loguru（API 更友好但需全面替换）。团队已有 logging 基础设施选 structlog；新项目无历史包袱选 loguru。

### 企业规模（平台/多租户 SaaS）

**需要**完整的可观测性栈、警报体系、合规持久化、高可用部署。

| 维度 | 做法 |
|------|------|
| 测试 | 完整三层测试金字塔，CI 中运行单元+集成，Nightly 运行 E2E |
| 日志 | 结构化 JSON → Kafka → ELK/Loki，支持按 session_id/tenant_id 检索 |
| 指标 | Prometheus + Grafana + AlertManager，Datadog（如已有合同） |
| Trace | OpenTelemetry Collector + Langfuse（LLM 专用）+ Grafana Tempo |
| 部署 | Kubernetes，HPA 自动扩缩，Readiness/Liveness Probe |
| CI/CD | 完整的 Pipeline：lint → typecheck → unit test → build image → integration test → deploy staging → e2e → deploy production |
| 凭据 | AWS Secrets Manager / HashiCorp Vault / Azure Key Vault |
| Session 持久化 | S3（按 session_id 路径存储 EventLog） + PostgreSQL（索引元数据，支持按租户/时间范围查询） |
| 告警 | 多层告警：LLM API 错误率、Token 消耗异常飙升、Session 超时率、Compaction 频率突变 |
| 多租户 | tenant_id 贯穿所有日志、指标 Labels、Trace Attributes |

**架构图示（企业级数据流）**：

```
Agent Instance (Pod)
  ├── OpenTelemetry SDK → OTLP Collector → Langfuse / Tempo
  ├── Prometheus Client → Prometheus → Grafana
  ├── structlog JSON → stdout → Fluentd → Kafka → ELK / S3
  └── SessionEvent → S3 (cold storage) + PostgreSQL (hot query)

AlertManager → PagerDuty / Slack / 飞书
```

---

## 部署考虑

### Session 事件日志持久化

Session 事件日志是 Harness 的核心资产，必须可靠持久化。

**存储策略**：
- **S3 / 对象存储**：适合冷数据。按 `s3://bucket/sessions/{date}/{session_id}.jsonl` 组织，生命周期策略自动归档/删除
- **PostgreSQL**：适合热查询。只存元数据索引（session_id、status、started_at、token_total、tenant_id），热点字段建立索引
- **双重写**：Agent 本地写 JSON Lines 文件（防网络中断丢失），后台异步上传到 S3

### Harness 无状态重启

Harness 的架构天然支持 crash recovery——不需要保存 Agent 进程的内存状态，只需要：

1. **Crash 发生**：Agent 进程异常退出
2. **新实例启动**：新进程从 SessionEvent 存储中读取最近一次 Session 的事件序列
3. **Session 重建**：重放 SessionEvent 流，将内存状态（消息列表、turn_count、token 计数）恢复到 crash 前的最后一个检查点
4. **继续执行**：从下一个 turn 开始，向 LLM 发送"中断恢复"提示，继续完成任务

这要求 SessionEvent 必须是 append-only 且不可变——一旦写入就不能修改。如果 crash 发生在 LLM 调用中（请求已发出但响应未收到），则丢弃该 turn、重试整个请求。

### 凭据管理

| 环境 | 方案 | 说明 |
|------|------|------|
| 本地开发 | `.env` 文件 | 加载到 `os.environ`，`.gitignore` 必须排除 |
| Staging | CI/CD Secret Variables | GitHub Actions Secrets → 注入到测试环境变量 |
| 生产环境 | Secrets Manager | AWS Secrets Manager / Vault，运行时通过 SDK 获取，自动轮转 |
| 本地模型（免凭据） | 不需要 | llama.cpp / Ollama 等本地部署模型无凭据管理需求 |

**通用原则**：凭据永远不入代码仓库、不入容器镜像、不入日志。企业级需要支持凭据轮转——Secrets Manager 返回临时凭证，Harness 需实现"凭据过期 → 透明重取 → 重试请求"的逻辑。

### 健康检查与优雅关闭

**Kubernetes Probe 定义**：
- `livenessProbe: /health` — 进程是否存活（返回 200 即存活，不检查 LLM 连接）
- `readinessProbe: /ready` — 是否可接收入站请求（检查 LLM API Key 是否有效、数据库连接是否正常）
- `startupProbe: /startup` — 初始启动完成的标志（预热模型连接，给予更长 initialDelaySeconds）

**优雅关闭**：
- 收到 SIGTERM → 标记不接收新 Session → 等待当前活跃 Session 完成或超时 → 持久化最后状态 → 退出
- 设置 `terminationGracePeriodSeconds` 大于"最大 Session 预期时长 + 持久化时间"

---

## 检查清单

- [ ] Agent 核心循环的单元测试：覆盖正常对话、带工具调用、Compaction 触发三种场景
- [ ] Mock LLMClient 支持预设多轮响应序列（list of LLMResponse）
- [ ] 集成测试覆盖 Session 持久化 → 恢复的完整链路
- [ ] 日志输出为结构化 JSON（非字符串格式化），每条日志携带 session_id
- [ ] LLM 调用前后有 Span 包裹，Span 属性包含 model、provider、latency、token_count
- [ ] Prometheus Histogram 记录 LLM 调用延迟，bucket 设置合理
- [ ] Compaction 触发次数和压缩比被记录为 Counter
- [ ] `/metrics` 端点可被 Prometheus 抓取，`/health` 和 `/ready` 端点正确实现
- [ ] `.env` 文件在 `.gitignore` 中，CI/CD 使用 Secret Variables
- [ ] Docker Compose 包含 Agent + Prometheus + Grafana 完整可观测栈
- [ ] SessionEvent 有持久化策略（文件/S3/数据库至少一种）
- [ ] 优雅关闭：SIGTERM 不丢失进行中的 Session 状态
- [ ] Grafana Dashboard 包含：Token 消耗趋势图、延迟热力图、工具成功率面板

---

## 常见陷阱

### 陷阱 1：日志用字符串拼接而非结构化

**症状**：`logger.info(f"Session {session_id}: LLM call took {latency}s")`

**问题**：无法按 session_id 聚合检索，延迟值嵌在字符串中无法被日志系统提取为指标。

**修正**：`logger.info("llm.call.completed", session_id=session_id, latency_ms=latency_ms)` —— 每个字段独立。

### 陷阱 2：把 SessionEvent 当"可选项"

**症状**：先是"先跑通再补日志"，然后永远没补。

**问题**：Session 事件日志是 Harness 架构的一部分，不是事后附加物。没有它，crash recovery、审计、成本归因全部失效。

**修正**：在 AgentCore 的 run() 方法中，SessionEvent 的 emit 应该和 LLM 调用同样优先级——缺省实现可以是空操作（Minimal 规模），但接口必须预留。

### 陷阱 3：生产环境使用 DEBUG 日志级别

**症状**：生产日志量爆炸，磁盘满、查询慢。

**问题**：LLM Agent 的 DEBUG 日志包含完整 prompt 和 response，单条可达数万字符。

**修正**：生产默认 INFO，敏感或不必要的内容仅在 DEBUG 输出。支持运行时按 session_id 临时打开 DEBUG（用于线上问题定位）。

### 陷阱 4：将 API Key 写入配置文件

**症状**：`config.yaml` 中包含 `api_key: "sk-xxx"`。

**问题**：迟早会被提交到 Git，或被 CI 日志输出。

**修正**：配置文件只定义 key 引用名（如 `api_key_from: "AWS_SECRET_LLM_KEY"`），实际值从环境变量或 Secrets Manager 运行时获取。

### 陷阱 5：忽视 Compaction 的观测

**症状**：只有 LLM 和 Tool 被监控，Compaction 是"隐形操作"。

**问题**：Compaction 是 Agent 长对话的核心机制，压缩质量直接影响后续 Agent 性能。缺少压缩频率和压缩比指标无法评估其有效性。

**修正**：Compaction 触发时记录 Span + Counter + 日志事件，携带 before_message_count、after_message_count、压缩耗时。

### 陷阱 6：测试中 Mock 掉了整个 AgentCore

**症状**：`assert mock_agent.run.called` —— 测试的是 Mock 对象而非真实逻辑。

**问题**：Agent 循环的逻辑（状态机迁移、终止条件判断）完全没有被测试。

**修正**：Mock 只应用于 LLMClient 和外部工具，AgentCore 本身保持真实实例。注入预设 LLMResponse 序列驱动循环。

### 陷阱 7：Span 结构扁平化

**症状**：所有 Span 都是根 Span，没有父子关系。

**问题**：无法看出"这次 Tool 调用是由哪轮 LLM 触发的"，丢失因果关系。

**修正**：严格建立 Span 层级 —— session → turn → (llm_call | tool_exec | compaction)。使用 OpenTelemetry 的 context propagation 自动维护父子关系。