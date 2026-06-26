# M-A3 30-Agent集群 通信协议规范
> 版本：v1.0 | 日期：2026-04-14

---

## 一、协议概述

### 1.1 设计目标
- **可靠性**：消息可靠投递，支持重试和确认
- **可追踪性**：全链路 trace_id，支持逆向追溯
- **高效性**：支持并行/串行动态切换
- **安全性**：消息加密 + 权限校验

### 1.2 协议层次

```
┌─────────────────────────────────────────────────────┐
│              Agent Message Protocol (AMP)            │
├─────────────────────────────────────────────────────┤
│  Layer 4: 业务语义层  (Task/Broadcast/Event/Ack)     │
│  Layer 3: 路由层     (P2P/Broadcast/Fan-out)         │
│  Layer 2: 可靠性层   (Retry/Ack/Timeout/Dedup)      │
│  Layer 1: 传输层     (HTTP-LongPoll/WebSocket/gRPC) │
└─────────────────────────────────────────────────────┘
```

---

## 二、消息格式

### 2.1 AgentMessage 结构

```python
from dataclasses import dataclass, field
from typing import Optional, Any
from datetime import datetime

@dataclass
class AgentMessage:
    # ── 身份标识 ──────────────────────────────────────
    msg_id: str                         # 全局唯一消息ID (UUIDv7)
    trace_id: str                       # 全链路追踪ID
    span_id: str                        # 当前操作ID
    parent_span_id: Optional[str]       # 父操作ID (顶级无parent)
    
    # ── 通信元数据 ─────────────────────────────────────
    sender: str                         # 发送方Agent ID
    receiver: str                       # 接收方Agent ID ("*" = 广播)
    msg_type: str                       # REQUEST/RESPONSE/BROADCAST/EVENT/ACK
    priority: int                       # 1-5 (1最高)
    
    # ── 业务载荷 ───────────────────────────────────────
    action: str                         # 操作类型 (见操作清单)
    payload: dict                       # 消息内容
    expected_response_format: Optional[dict] = None  # 响应格式约定
    
    # ── 可靠性 ─────────────────────────────────────────
    ttl_seconds: int = 300              # 生存时间
    retry_count: int = 0                # 已重试次数
    max_retries: int = 3                # 最大重试次数
    correlation_id: Optional[str] = None # 关联请求ID (用于响应匹配)
    
    # ── 安全 ───────────────────────────────────────────
    auth_token: Optional[str] = None
    pii_present: bool = False           # 是否含敏感信息
    
    # ── 时间戳 ─────────────────────────────────────────
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    expires_at: Optional[str] = None

# ── 消息类型枚举 ──────────────────────────────────────
class MsgType:
    REQUEST   = "REQUEST"    # 请求-响应模式
    RESPONSE  = "RESPONSE"   # 响应消息
    BROADCAST = "BROADCAST"  # 广播（无响应期望）
    EVENT     = "EVENT"      # 事件通知（异步）
    ACK       = "ACK"        # 确认消息

# ── 操作类型清单 ──────────────────────────────────────
class AgentAction:
    # 通用
    HEALTH_CHECK    = "health_check"
    REPORT_STATUS   = "report_status"
    FETCH_DATA      = "fetch_data"
    
    # GEO域
    MARKET_RESEARCH = "market_research"
    COMPETITOR_ANALYSIS = "competitor_analysis"
    CONTENT_STRATEGY = "content_strategy"
    MULTILINGUAL_OPT = "multilingual_optimization"
    PLATFORM_ADAPT   = "platform_adaptation"
    MONITORING       = "geo_monitoring"
    KNOWLEDGE_GRAPH  = "knowledge_graph_build"
    INTENT_PREDICT   = "intent_prediction"
    SCHEMA_OPT       = "schema_optimization"
    REGIONAL_STRATEGY = "regional_strategy"
    
    # 亚马逊域
    PRODUCT_SELECT   = "product_selection"
    LISTING_OPT      = "listing_optimization"
    PROFIT_OPT       = "profit_optimization"
    ADS_MANAGE       = "ads_management"
    INVENTORY_MANAGE = "inventory_management"
    REVIEW_ANALYSIS  = "review_analysis"
    COMPETITOR_MONITOR = "competitor_monitoring"
    PRICING_STRATEGY = "pricing_strategy"
    KEYWORD_RESEARCH = "keyword_research"
    REPORTING        = "report_generation"
    
    # 支撑域
    DATA_COLLECT     = "data_collection"
    CONTENT_GENERATE  = "content_generation"
    TRANSLATE         = "translation"
    COMPLIANCE_CHECK  = "compliance_check"
    REPORT_GENERATE   = "report_generate"
    CUSTOMER_SERVICE  = "customer_service"
    QUALITY_SCORING   = "quality_scoring"
    MEMORY_MANAGE     = "memory_management"
    SCHEDULE_TASK     = "schedule_task"
    SECURITY_AUDIT    = "security_audit"
```

### 2.2 响应格式

```python
@dataclass
class AgentResponse:
    msg_id: str                        # 对应请求的 msg_id
    trace_id: str                      # 继承请求的 trace_id
    span_id: str                       # 响应操作的 span_id
    
    status: str                        # SUCCESS / PARTIAL / FAILED / TIMEOUT
    error_code: Optional[str] = None   # 错误码
    error_message: Optional[str] = None
    
    result: Optional[Any] = None       # 业务结果
    quality_score: Optional[float] = None  # SUP-07评分
    
    metadata: dict = field(default_factory=dict)
    # metadata 可包含: execution_time_ms, tokens_used, agent_id
    
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
```

---

## 三、路由模式

### 3.1 路由类型

| 模式 | 说明 | 使用场景 |
|------|------|---------|
| `P2P` | 点对点，一对一 | 明确的下游Agent |
| `FAN_IN` | 多对一，聚合 | 结果汇总 |
| `FAN_OUT` | 一对多，并行 | 多域并行启动 |
| `BROADCAST` | 广播至所有Agent | 系统公告/安全事件 |
| `DOMAIN_BROADCAST` | 域内广播 | GEO域内通知 |

### 3.2 路由配置示例

```yaml
# 典型任务路由配置
routing_templates:
  # 场景1：新品上市全链路（GEO + 亚马逊并行）
  new_product_launch:
    parallel_groups:
      - domain: "geo"
        agents: ["geo-01-market-research", "geo-02-competitor"]
        mode: "PARALLEL"
      - domain: "amazon"
        agents: ["amz-01-product-select"]
        mode: "PARALLEL"
    dependencies:
      - from: "geo-01-market-research"
        to: "geo-03-content-strategy"
      - from: "geo-02-competitor"
        to: "geo-03-content-strategy"
      - from: ["geo-01-market-research", "amz-01-product-select"]
        to: "sup-09-scheduler"
        mode: "FAN_IN"

  # 场景2：竞品动态监控
  competitor_monitoring:
    agents: ["amz-07-competitor-monitor"]
    schedule: "cron:0 * * * *"  # 每小时
    downstream:
      - agent: "amz-08-pricing"
        condition: "price_change > 5%"
      - agent: "amz-04-ads"
        condition: "competitor_rank_change"

  # 场景3：质量问题升级
  quality_escalation:
    trigger: "quality_score < 60"
    agents: ["sup-07-quality", "sup-10-security"]
    notify: "chief-of-staff"
    severity: "high"
```

---

## 四、可靠性机制

### 4.1 重试策略

```python
RETRY_CONFIG = {
    "max_retries": 3,
    "backoff": {
        "type": "exponential",
        "initial_ms": 1000,
        "multiplier": 2.0,
        "max_ms": 30000,
        "jitter": True  # ±10%随机抖动避免惊群
    },
    "retryable_errors": [
        "NETWORK_ERROR",
        "TIMEOUT",
        "SERVICE_UNAVAILABLE",
        "RATE_LIMITED"
    ],
    "non_retryable_errors": [
        "INVALID_REQUEST",
        "UNAUTHORIZED",
        "FORBIDDEN",
        "NOT_FOUND"
    ]
}
```

### 4.2 幂等性保证

```python
# 每个 REQUEST 消息携带 idempotency_key
# 接收方基于 (sender, action, idempotency_key) 做去重
# 相同key的重复请求直接返回缓存响应

@dataclass
class IdempotencyRecord:
    key: str              # hash(msg_id)
    request_hash: str     # hash(payload)
    response: AgentResponse
    created_at: datetime
    expires_at: datetime  # TTL=3600s
```

### 4.3 超时配置

```python
TIMEOUT_CONFIG = {
    # P2P 请求超时（按操作类型）
    "P2P_DEFAULT": 30,          # 秒
    "market_research": 300,
    "knowledge_graph_build": 600,
    "data_collection": 600,
    "content_generation": 300,
    "listing_optimization": 300,
    "translation": 120,
    "health_check": 5,
    "memory_management": 60,
    "quality_scoring": 120,
    
    # 整链路超时（按场景）
    "GEO_FULL_PIPELINE": 1800,   # 30分钟
    "AMAZON_FULL_PIPELINE": 1800,
    "NEW_PRODUCT_LAUNCH": 3600   # 60分钟
}
```

---

## 五、安全协议

### 5.1 消息加密

```python
# 所有跨域消息必须加密
MESSAGE_SECURITY = {
    "encryption": "AES-256-GCM",      # 消息体加密
    "signature": "HMAC-SHA256",       # 完整性校验
    "key_exchange": "ECDH-P256",      # 密钥协商
    
    # Token格式
    "token_format": "Bearer {jwt}",
    "jwt_algorithm": "RS256",
    "token_expiry_seconds": 3600,
    
    # 敏感字段
    "pii_fields": ["email", "phone", "id_card", "bank_account", "api_key"],
    "pii_action": "MASK"              # MASK/REJECT/LOG
}
```

### 5.2 权限矩阵

```python
# Agent间调用权限 (简化示例)
PERMISSION_MATRIX = {
    # 格式: (caller, action, resource) -> allowed
    # 各Agent调用基础设施Agent
    ("*", "health_check", "sup-10-security"): True,
    ("*", "security_audit", "sup-10-security"): True,
    ("*", "fetch_data", "sup-01-data-collect"): True,
    ("*", "memory_management", "sup-08-memory"): True,
    
    # 数据流权限
    ("geo-01-market-research", "REQUEST", "sup-01-data-collect"): True,
    ("amz-01-product-select", "REQUEST", "sup-01-data-collect"): True,
    
    # 质量监控
    ("*", "quality_scoring", "sup-07-quality"): True,
    
    # 跨域数据流
    ("geo-01-market-research", "REQUEST", "amz-01-product-select"): True,  # GEO→Amazon数据共享
    ("amz-06-review", "FETCH_DATA", "geo-07-knowledge-graph"): True,      # Amazon→GEO反馈
    
    # 默认拒绝
    ("*", "*", "*"): False
}
```

---

## 六、Trace 协议

### 6.1 TraceContext

```python
@dataclass
class TraceContext:
    trace_id: str         # 64位UUID，贯穿整条请求链路
    span_id: str          # 8位十六进制，当前操作ID
    parent_span_id: Optional[str] = None  # 父span
    
    # 传播字段 (HTTP Header: traceparent)
    # traceparent: 00-{trace_id}-{span_id}-{flags}
    # flags: 01=采样, 00=不采样

# ── Span生命周期 ──────────────────────────────────────
# 开始: span_id = generate_span_id()
# 进行中: 记录 start_time + 关键事件
# 结束: 记录 end_time + status + attributes
# 导出: 异步写入 SQLite + JSONL.gz
```

### 6.2 Trace传播示例

```
用户: "帮我分析某产品在北美市场的机会"
  │
  ▼
[trace_id: abc123] chief-of-staff.intent-recognition (span: 00000001)
  │
  ├──▶ [并行执行组 1]
  │     ├─ geo-01-market-research (span: 00000002, parent: 00000001)
  │     │      ├─ sup-01-data-collect (span: 00000003, parent: 00000002) ✓
  │     │      └─ [结果: 市场容量报告] (耗时: 2.3s)
  │     │
  │     └─ amz-01-product-select (span: 00000004, parent: 00000001)
  │            ├─ sup-01-data-collect (span: 00000005, parent: 00000004) ✓
  │            └─ [结果: 选品分析] (耗时: 2.8s)
  │
  └──▶ [等待依赖完成] → geo-03-content-strategy (span: 00000006, parent: 00000001)
         ├─ geo-04-multilingual (span: 00000007, parent: 00000006) ✓
         ├─ sup-02-content-gen (span: 00000008, parent: 00000006) ✓
         └─ [结果: 内容策略报告] (耗时: 1.5s)
  
  ▼
  chief-of-staff.result-aggregation (span: 00000009, parent: 00000001)
  ├─ sup-05-report-gen (span: 00000010) ✓
  └─ [最终报告] (总耗时: 8.2s)
```

---

## 七、API接口

### 7.1 Agent请求接口

```yaml
POST /api/v1/agent/execute
Content-Type: application/json
Authorization: Bearer {jwt}

Request:
{
  "sender": "chief-of-staff",
  "receiver": "geo-01-market-research",
  "msg_type": "REQUEST",
  "action": "market_research",
  "priority": 1,
  "payload": {
    "product": "无线蓝牙耳机",
    "regions": ["北美", "欧盟", "东南亚"],
    "date_range": "2024-01-01~2026-03-31"
  },
  "trace_id": "abc123-def456",
  "span_id": "00000001",
  "ttl_seconds": 300,
  "idempotency_key": "req-20260414-001"
}

Response (200 OK):
{
  "msg_id": "msg-uuid-xxx",
  "trace_id": "abc123-def456",
  "status": "SUCCESS",
  "result": {
    "market_size": "TAM=$12.5B, SAM=$3.2B, SOM=$480M",
    "top_regions": ["北美", "东南亚", "中东"],
    "growth_rate": "+18% YoY",
    "quality_score": 87.5
  },
  "quality_score": 87.5,
  "metadata": {
    "execution_time_ms": 2314,
    "tokens_used": 4521,
    "agent_id": "geo-01-market-research"
  }
}
```

### 7.2 批量请求接口

```yaml
POST /api/v1/agent/batch-execute
Authorization: Bearer {jwt}

Request:
{
  "execution_mode": "PARALLEL",  # PARALLEL / SEQUENTIAL / DAG
  "tasks": [
    {"receiver": "geo-01", "action": "market_research", "payload": {...}},
    {"receiver": "amz-01", "action": "product_select", "payload": {...}},
    {"receiver": "sup-01", "action": "data_collect", "payload": {...}}
  ],
  "dependencies": [
    {"from": "geo-01", "to": "geo-03", "condition": "always"}
  ],
  "max_parallel": 10
}

Response (200 OK):
{
  "batch_id": "batch-xxx",
  "execution_plan": [...],  # DAG可视化
  "results": {
    "geo-01": {"status": "SUCCESS", "result": {...}},
    "amz-01": {"status": "SUCCESS", "result": {...}},
    "sup-01": {"status": "PENDING", "estimated_start": "2026-04-14T10:00:00Z"}
  }
}
```

---

## 八、健康检查与监控

### 8.1 Agent健康检查

```python
# /health/{agent_id} 接口响应格式
{
    "agent_id": "geo-01-market-research",
    "status": "HEALTHY",  # HEALTHY / DEGRADED / DOWN
    "version": "1.0.0",
    "uptime_seconds": 86400,
    "metrics": {
        "requests_total": 1523,
        "requests_success": 1498,
        "requests_failed": 25,
        "avg_latency_ms": 2340,
        "p95_latency_ms": 5100,
        "error_rate": 0.016,
        "queue_depth": 3,
        "active_connections": 12
    },
    "dependencies": {
        "sup-01-data-collect": "HEALTHY",
        "sup-08-memory": "HEALTHY"
    },
    "last_heartbeat": "2026-04-14T10:00:05Z"
}
```

### 8.2 告警规则

```yaml
alerts:
  - name: "agent_down"
    condition: "status == DOWN"
    severity: "CRITICAL"
    channels: ["slack", "email", "pagerduty"]
    
  - name: "high_error_rate"
    condition: "error_rate > 0.05"
    severity: "WARNING"
    channels: ["slack"]
    
  - name: "high_latency"
    condition: "p95_latency > 10000"
    severity: "WARNING"
    channels: ["slack"]
    
  - name: "queue_overflow"
    condition: "queue_depth > 50"
    severity: "CRITICAL"
    channels: ["slack", "pagerduty"]
    
  - name: "security_event"
    condition: "event_type == UNAUTHORIZED_ACCESS"
    severity: "CRITICAL"
    channels: ["security-team", "pagerduty"]
```

---

*本协议规范为 M-A3 30-Agent集群 的通信标准*
*版本 v1.0 | 2026-04-14*
