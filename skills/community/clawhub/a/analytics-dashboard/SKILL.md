---
name: analytics-dashboard
description: "数据看板查询Skill，通过dashboard-mcp获取实时统计/系统健康/租户概览/内容队列/事件订阅等看板数据。触发:数据看板/实时统计/系统健康/租户概览/内容队列/事件订阅/早朝简报/Agent状态 不触发:内容发布/商品管理/Cookie管理"
version: 1.0.0
user-invocable: true
tools: [read]
dependencies: []
metadata:
  layer: plugin
  priority: P1
  category: analytics
  openclaw:
    emoji: "📊"
    os: ["win32", "linux", "darwin"]
    requires:
      bins: ["python"]
      config: ["mcp.servers.dashboard-mcp"]
      env: []
---

> **核心功能**: 本技能提供/Cookie管理等能力。


# Analytics Dashboard Skill

数据看板查询引擎，通过dashboard-mcp统一获取系统运营数据看板(R-82 Skill连接补全)。**状态**: 🟢已实现 | **优先级**: P1

## 使用场景

1. 实时看板: 查询系统实时统计(活跃状态/内容管道数/告警数)
2. 系统健康: 检查Docker/Gateway/磁盘健康状态
3. 租户概览: 查询指定租户的发布量和最近发布记录
4. 内容队列: 查询租户内容队列状态(待处理/处理中/完成/失败)
5. 事件订阅: 获取最近N条系统事件(告警/KPI/设备)
6. Agent状态: 查询所有Agent运行状态
7. 早朝简报: 获取每日早朝简报数据

## 工作流

### 实时看板查询(realtime)
1. 接收请求(action=realtime)
2. 调用dashboard-mcp的`get_realtime_stats`工具获取实时统计
3. 返回live_status + content_pipelines_24h + pending_alerts

### 系统健康检查(health)
1. 接收请求(action=health)
2. 调用dashboard-mcp的`get_system_health`工具获取健康状态
3. 返回Docker/Gateway/Disk健康状态+overall判定(healthy/degraded)

### 租户概览查询(tenant)
1. 接收请求(action=tenant, tenant_id=<参数>)
2. 调用dashboard-mcp的`get_tenant_overview`工具，传入tenant_id
3. 返回租户信息+总发布量+最近5条发布记录

### 内容队列状态(queue)
1. 接收请求(action=queue, tenant_id=<参数>)
2. 调用dashboard-mcp的`get_content_queue_status`工具，传入tenant_id
3. 返回队列总数+各状态计数(pending/processing/completed/failed)

### 事件订阅(events)
1. 接收请求(action=events, event_type=all, limit=50)
2. 调用dashboard-mcp的`subscribe_events`工具，传入event_type和limit
3. 返回最近N条事件(最新在前)

### Agent状态查询(agents)
1. 接收请求(action=agents)
2. 调用dashboard-mcp的`get_agents_status`工具获取所有Agent状态
3. 返回Agent总数+各Agent状态+live_status

## 数据源

> 统一数据查询入口：通过dashboard-mcp(R-82)获取看板数据，禁止Skill自行读取data/下数据文件，消除碎片化

| 数据类型 | 获取方式 | dashboard-mcp工具 |
|:---------|:---------|:------------------|
| 实时统计 | dashboard-mcp `get_realtime_stats` | 聚合live_status+管道数+告警数 |
| 系统健康 | dashboard-mcp `get_system_health` | Docker/Gateway/Disk(复用health_checks) |
| 租户概览 | dashboard-mcp `get_tenant_overview` | 发布量+最近发布 |
| 内容队列 | dashboard-mcp `get_content_queue_status` | 队列状态计数 |
| 事件订阅 | dashboard-mcp `subscribe_events` | 最近N条事件(alert_queue.jsonl) |
| Agent状态 | dashboard-mcp `get_agents_status` | Agent列表+live_status |

## 异常处理

| 异常 | 错误码 | 处理 |
|:-----|:-------|:-----|
| dashboard-mcp不可用 | MCP_UNAVAILABLE | 返回降级提示，建议检查dashboard-mcp容器状态 |
| tenant_id为空 | TENANT_ID_EMPTY | 提示"租户ID必填" |
| 数据文件不存在 | DATA_NOT_FOUND | 返回空数据+提示"暂无数据" |
| MCP调用超时 | MCP_TIMEOUT | circuit_breaker熔断，返回最近缓存数据 |
| 工具参数无效 | INVALID_PARAMS | 提示参数格式要求 |

## 输入格式

```json
{
  "action": "realtime|health|tenant|queue|events|agents",
  "tenant_id": "<参数>",
  "event_type": "all|kpi|alert|device",
  "limit": 50
}
```

字段说明:
- `action`: 操作类型(realtime实时看板/health系统健康/tenant租户概览/queue内容队列/events事件订阅/agents状态查询)
- `tenant_id`: 租户ID(tenant/queue操作必填)
- `event_type`: 事件类型(events操作使用,默认all)
- `limit`: 返回条数(events操作使用,默认50,最大500)

## 输出格式

```json
{
  "success": true,
  "data": {
    "action": "realtime",
    "live_status": {},
    "content_pipelines_24h": 5,
    "pending_alerts": 2,
    "timestamp": "2026-07-17T10:00:00Z"
  },
  "error": null,
  "code": null
}
```

字段说明:
- `live_status`: 系统活跃状态对象
- `content_pipelines_24h`: 近24小时内容管道数
- `pending_alerts`: 待处理告警数
- `timestamp`: 数据获取时间(ISO格式)

## 示例

### 示例1: 实时看板查询

1. 调用realtime → dashboard-mcp `get_realtime_stats` → 返回实时统计
2. 返回: `{success:true, data:{live_status:{}, content_pipelines_24h:5, pending_alerts:2, timestamp:"..."}}`

### 示例2: 租户概览查询

1. 调用tenant(tenant_id="t001") → dashboard-mcp `get_tenant_overview("t001")` → 返回租户概览
2. 返回: `{success:true, data:{tenant_id:"t001", total_publishes:42, recent_publishes:[...], timestamp:"..."}}`

### 示例3: 系统健康检查

1. 调用health → dashboard-mcp `get_system_health` → 返回健康状态
2. 返回: `{success:true, data:{docker:{healthy:true}, gateway:{healthy:true}, disk:{}, overall:"healthy", timestamp:"..."}}`

## 关联文档

- dashboard-mcp: mcps/dashboard-mcp/server.py (20个工具, DEF-85阶段2)
- 05文档§四 DEF-07 (dashboard迁移设计)
- SKILL_REGISTRY: agents/hubu/SKILL_REGISTRY.md (已注册)

## 变更历史

| 版本 | 日期 | 变更说明 |
|:-----|:-----|:---------|
| v1.0.0 | 2026-07-17 | B2-09: 创建analytics-dashboard Skill连接dashboard-mcp(R-82), 封装6核心看板查询工具, 补全hubu SKILL_REGISTRY已注册但缺失的Skill文件 |
