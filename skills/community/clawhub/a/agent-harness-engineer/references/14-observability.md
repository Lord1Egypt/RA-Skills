# 可观测性设计

> Observability = The ability to understand the internal state of a system from its external outputs.
> For Agent Harness: Traces show what happened, Metrics show how well, Logs show why.

---

## 三支柱架构

```
                    ┌───────────────────────────────────┐
                    │          Agent Harness             │
                    │                                    │
                    │  ┌─────────┐ ┌────────┐ ┌───────┐ │
                    │  │  Trace  │ │Metrics │ │ Logs  │ │
                    │  │ (链路)  │ │ (指标) │ │(日志) │ │
                    │  └────┬────┘ └───┬────┘ └───┬───┘ │
                    │       │          │          │      │
                    └───────┼──────────┼──────────┼──────┘
                            │          │          │
              ┌─────────────┼──────────┼──────────┼──────────────┐
              │             ▼          ▼          ▼              │
              │     ┌──────────┐ ┌──────────┐ ┌──────────┐      │
              │     │Langfuse  │ │Prometheus│ │  Loki /  │      │
              │     │(LLM 追踪)│ │(指标收集)│ │  ELK     │      │
              │     └──────────┘ └──────────┘ └──────────┘      │
              │                             │                    │
              │                        ┌────▼────┐              │
              │                        │ Grafana │              │
              │                        │(可视化) │              │
              │                        └─────────┘              │
              │              Observability Stack                │
              └────────────────────────────────────────────────┘
```

### 三支柱关系

| 支柱 | 回答的问题 | 数据粒度 | 保留周期 | Agent 独有挑战 |
|---|---|---|---|---|
| **Trace** | "这个请求经历了什么？" | 单次请求级 | 7-30天 | LLM 调用的 token/成本追踪 |
| **Metrics** | "系统整体健康吗？" | 聚合统计级 | 90-365天 | 工具调用成功率分解 |
| **Logs** | "具体发生了什么？" | 事件/消息级 | 7-90天 | 权限决策的审计记录 |

---

## Trace (链路追踪)

### Span 层级模型

```
Session Span (整个会话)
├── Turn Span #1 (第 1 轮)
│   ├── LLM Call Span (模型推理)
│   │   ├── Token Usage: {input: 1500, output: 300}
│   │   └── Cost: $0.003
│   ├── Tool Use Span: write_file (工具调用)
│   │   ├── Duration: 45ms
│   │   ├── Status: success
│   │   └── File: server.py (332 bytes)
│   ├── Permission Check Span (权限检查)
│   │   ├── Tool: write_file
│   │   └── Decision: allowed (by rule)
│   └── Tool Use Span: bash (工具调用)
│       ├── Duration: 2300ms
│       ├── Status: success
│       └── Command: pip install flask
├── Turn Span #2
│   └── ...
└── Session Summary
    ├── Total Turns: 5
    ├── Total Tokens: 12000
    └── Total Cost: $0.025
```

### OpenTelemetry Span 属性规范

| Span 类型 | 关键属性 | 示例值 |
|---|---|---|
| `agent.session` | `session.id`, `agent.model`, `agent.version` | `session-abc123`, `claude-4`, `1.2.0` |
| `agent.turn` | `turn.number`, `turn.reason` | `3`, `user_initiated` |
| `llm.call` | `llm.model`, `llm.temperature`, `llm.input_tokens`, `llm.output_tokens`, `llm.cost`, `llm.latency_ms` | `claude-4`, `0.7`, `1500`, `300`, `0.003`, `1200` |
| `tool.execute` | `tool.name`, `tool.status`, `tool.duration_ms`, `tool.error_type` | `write_file`, `success`, `45`, `null` |
| `permission.check` | `permission.tool`, `permission.path`, `permission.decision` | `write_file`, `/app/config.json`, `allowed` |
| `compaction` | `compaction.reason`, `compaction.messages_before`, `compaction.messages_after` | `context_limit`, `50`, `30` |

### Langfuse 集成 (LLM 专用追踪)

Langfuse 负责 LLM 调用级别的详细追踪，超越通用 OpenTelemetry 的能力：

| 追踪维度 | OpenTelemetry | Langfuse |
|---|---|---|
| Token 用量分解 (input/output) | ✅ | ✅ (自动捕获) |
| 每次调用的成本估算 | ❌ | ✅ (内置 pricing) |
| 缓存命中率 | ❌ | ✅ (Cache read/write tokens) |
| Prompt 版本追踪 | ❌ | ✅ (Prompt management) |
| 评测数据关联 | ❌ | ✅ (Datasets + Scores) |

---

## Metrics (指标)

### 7 项核心指标

#### 1. Token 消耗率

```
指标名称: agent_tokens_total
类型: Counter
标签 (Labels): {session_id, model, token_type: input|output}
导出频率: 每个 turn_end 时增量更新
用途: 成本预测、模型选择优化
```

#### 2. LLM 延迟

```
指标名称: agent_llm_latency_seconds
类型: Histogram
标签: {model, status: success|error}
Buckets: [0.1, 0.5, 1, 2, 5, 10, 30, 60, 120]
导出频率: 每次 LLM 调用完成
用途: SLO 监控、模型性能对比
告警阈值: p99 > 30s
```

#### 3. 工具调用成功率

```
指标名称: agent_tool_calls_total
类型: Counter (success + error 两个系列)
标签: {tool_name, status: success|error, error_type}
导出频率: 每次工具调用完成
用途: 工具稳定性分析、错误类型分布
告警阈值: success_rate < 90% (by tool_name) 持续 5 分钟
```

#### 4. 压缩频率

```
指标名称: agent_compactions_total
类型: Counter
标签: {reason: context_limit|cost_optimization|user_request}
导出频率: 每次压缩触发
用途: 上下文管理策略调整
告警阈值: > 10 次/分钟 (异常压缩风暴)
```

#### 5. 错误率

```
指标名称: agent_errors_total
类型: Counter
标签: {error_type: timeout|api_error|tool_error|permission_denied|unknown}
导出频率: 每次错误发生
用途: 系统健康度、错误趋势分析
告警阈值: 总错误率 > 5% 持续 5 分钟
```

#### 6. 会话时长

```
指标名称: agent_session_duration_seconds
类型: Histogram
标签: {status: completed|expired|error|cancelled}
Buckets: [30, 60, 120, 300, 600, 1800, 3600]
导出频率: 会话结束时
用途: 用户行为分析、资源规划
```

#### 7. 预估成本

```
指标名称: agent_estimated_cost_dollars_total
类型: Counter
标签: {model, session_id}
导出频率: 每个 turn_end 时更新
用途: 成本归因、按模型/用户分析
计算: 基于模型的公开定价 (input_tokens * price_in + output_tokens * price_out)
```

### Prometheus 导出端点

```
GET /metrics

输出格式:
# HELP agent_tokens_total Total tokens consumed
# TYPE agent_tokens_total counter
agent_tokens_total{session_id="abc123",model="claude-4",token_type="input"} 15000
agent_tokens_total{session_id="abc123",model="claude-4",token_type="output"} 3200
# HELP agent_llm_latency_seconds LLM call latency
# TYPE agent_llm_latency_seconds histogram
agent_llm_latency_seconds_bucket{model="claude-4",le="1"} 150
agent_llm_latency_seconds_bucket{model="claude-4",le="2"} 230
...
```

---

## Logs (日志)

### 结构化日志 Schema

```json
{
  "timestamp": "2025-01-15T10:30:02.350Z",
  "level": "INFO",
  "logger": "agent_harness.session",
  "event": "tool_result_received",
  "trace_id": "a1b2c3d4e5f6...",
  "session_id": "sess-abc123",
  "turn_number": 3,
  "context": {
    "tool_name": "write_file",
    "success": true,
    "duration_ms": 45,
    "file_size_bytes": 332
  }
}
```

### 日志级别使用规范

| 级别 | 含义 | 使用场景 | 环境 |
|---|---|---|---|
| **DEBUG** | 开发调试信息 | 工具调用参数详情、LLM prompt 全文、沙箱配置详情 | 开发环境 |
| **INFO** | 正常操作记录 | Turn 开始/结束、工具执行结果、权限检查通过 | 所有环境 |
| **WARN** | 需要关注但不影响功能 | 权限被拒绝、工具调用超时重试、压缩频繁触发、接近速率限制 | Staging + 生产 |
| **ERROR** | 功能异常 | 工具调用失败、LLM API 错误、沙箱崩溃、会话恢复失败 | 所有环境 |

### Context Binding (上下文绑定)

所有日志必须包含以下上下文字段（通过 `structlog.bind()` 或 `logger.child()` 实现）：

| 字段 | 来源 | 链路能力 |
|---|---|---|
| `trace_id` | 从 OpenTelemetry context 提取 | 关联 Trace |
| `session_id` | Session 对象 | 关联同一会话的所有日志 |
| `turn_number` | Session turn 计数器 | 定位具体轮次 |
| `model` (条件) | LLM 调用上下文 | 定位模型相关问题 |

---

## Session = 审计日志

Session 的 append-only 事件日志天然就是审计日志。无需为 Agent 操作建立独立的审计系统。

### 审计就绪矩阵

| 审计需求 | Session 事件日志覆盖 | 额外配置需求 |
|---|---|---|
| 操作时间线 | `timestamp` 字段 | 无 |
| 操作者身份 | `role: "user"` + Session 关联的用户 ID | 需在 Session 创建时绑定用户 |
| 工具调用记录 | `tool_use` + `tool_result` | 无 |
| 权限决策 | `permission.check` 事件 | 需在 Permission 模块中发射事件 |
| 数据访问记录 | `tool_use` 的 `tool_name=read` | 无 |
| 数据修改记录 | `tool_use` 的 `tool_name=edit` + `arguments` | 无 |
| 异常事件 | `tool_result.success=false` | 无 |
| 成本核算 | `turn_end.token_summary.total_cost` | 模型 pricing 表 |

---

## 告警规则 (Enterprise 级别)

| 告警名称 | 条件 | 严重级别 | 建议响应 |
|---|---|---|---|
| 高错误率 | `rate(agent_errors_total[5m]) / rate(agent_tool_calls_total[5m]) > 0.05` | Critical | 暂停 Agent 自动审批，切换人工审核 |
| LLM 高延迟 | `histogram_quantile(0.99, agent_llm_latency_seconds) > 30` | Warning | 检查 API 状态页，考虑降级到更快模型 |
| 压缩风暴 | `rate(agent_compactions_total[1m]) > 10` | Warning | 检查上下文大小配置，可能需增大 context window |
| 工具调用异常 | `rate(agent_tool_calls_total{status="error"}[5m]) > 0.1 * rate(agent_tool_calls_total[5m])` | Critical | 检查具体工具的错误分布，可能需回滚工具变更 |
| 成本异常 | `rate(agent_estimated_cost_dollars_total[1h]) > threshold` | Warning | 检查是否有 Agent 进入无限循环，需人工介入 |
| 会话积压 | `agent_active_sessions > max_concurrent * 0.8` | Warning | 扩容 Harness 实例或限流新会话 |

---

## 规模特定实现概要

### Minimal (~0 行)
```
无可观测性基础设施。
依赖 Agent 自身输出的文本作为调试依据。
仅适用于个人使用或一次性脚本。
```

### Professional (~100 行)
```
核心组件：
  - StructuredLogger: structlog (Python) / pino (Node)
  - BasicMetrics: Counter + Histogram (基于 prometheus-client)

实现要点：
  - 日志输出为 JSON 格式到 stdout/stderr
  - metrics 通过 /metrics 端点导出
  - trace_id 通过 contextvars 或 AsyncLocalStorage 传递
  - 不含 Grafana/Langfuse 集成
```

### Enterprise (~400 行)
```
核心组件：
  - OpenTelemetry SDK (自动插桩 + 手动 Span)
  - Prometheus + Grafana (指标采集 + 可视化)
  - Langfuse (LLM 专用追踪 + 成本分析)
  - Alertmanager (告警路由)

实现要点：
  - 配置 OTLP Exporter 指向 Collector
  - 在关键路径手动创建 Span (LLM call, tool execution, permission check)
  - 配置 Span → Log 关联 (注入 trace_id)
  - 配置 Grafana Dashboard (导入预定义 JSON 模板)
  - 配置告警规则文件 (.yml) 并加载到 Prometheus
  - 配置 Langfuse callback 拦截 LLM SDK 调用
```

---

⚠ **AI 构建提示**：

```
根据用户选择的规模实现可观测性：

Minimal 级别：
  跳过。不添加任何可观测性代码。

Professional 级别：
  1. 安装 structlog (Python) 或 pino (Node)
  2. 在入口处配置 JSON 格式输出
  3. 在所有关键事件处添加 logger.info(event="event_name", **context)
  4. 安装 prometheus-client (Python) 或 prom-client (Node)
  5. 添加 Counter: agent_tool_calls_total, agent_errors_total
  6. 添加 Histogram: agent_llm_latency_seconds
  7. 注册 /metrics HTTP 端点

Enterprise 级别：
  1. 安装 opentelemetry-api, opentelemetry-sdk, opentelemetry-exporter-otlp
  2. 配置 TracerProvider 和 OTLP Exporter
  3. 在所有工具调用包装器中创建 Span
  4. 安装 langfuse SDK 并配置 callback
  5. 在 LLM 调用处标记为 Langfuse Generation
  6. 导入 Grafana Dashboard JSON
  7. 配置 Prometheus 告警规则文件

检查清单：
  □ 每个 Span 包含必需的属性 (session_id, turn_number, etc.)
  □ 每行日志包含 trace_id 和 session_id
  □ /metrics 端点可被 Prometheus 抓取
  □ 告警规则配置文件格式正确
  □ Langfuse 回调不阻塞主流程 (异步发送)
```