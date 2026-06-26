---
name: consul-api
description: >
  Consul HTTP API operations for service discovery, key-value store, health checks, and service mesh management.
  Use when working with Consul clusters for: (1) Registering/querying services and nodes, (2) KV store operations,
  (3) Health check queries, (4) ACL token management, (5) Service mesh configuration, or any Consul-related API tasks.
---

# Consul API

HashiCorp Consul HTTP API 操作指南。提供服务发现、KV 存储、健康检查和服务网格管理能力。

## Quick Start

**Base URL:** `http://127.0.0.1:8500/v1/`

**认证方式:**
```bash
# 方式 1: X-Consul-Token header (推荐)
curl -H "X-Consul-Token: <token>" http://127.0.0.1:8500/v1/agent/members

# 方式 2: Bearer token
curl -H "Authorization: Bearer <token>" http://127.0.0.1:8500/v1/agent/members
```

**常用查询参数:**
- `dc` - 指定数据中心
- `ns` - 指定命名空间 (Enterprise)
- `pretty` - 格式化 JSON 输出
- `wait=<duration>` - 阻塞查询等待时间
- `index=<num>` - 阻塞查询索引

## Service Discovery (Catalog)

### 列出所有服务
```bash
GET /catalog/services
GET /catalog/services?dc=dc1
```
返回: `{"service-name": ["tag1", "tag2"], ...}`

### 查询服务的所有实例
```bash
GET /catalog/service/:service_name
GET /catalog/service/redis?dc=dc1&ns=default
```

### 列出所有节点
```bash
GET /catalog/nodes
GET /catalog/nodes?near=_agent
```

### 注册服务
```bash
PUT /catalog/register
{
  "Node": "node1",
  "Address": "192.168.1.1",
  "Service": {
    "Service": "redis",
    "ID": "redis-1",
    "Tags": ["primary", "v1"],
    "Address": "127.0.0.1",
    "Port": 6379
  }
}
```

### 注销服务
```bash
PUT /catalog/deregister
{
  "Node": "node1",
  "ServiceID": "redis-1"
}
```

## Key-Value Store

### 读取 KV
```bash
GET /kv/:key              # 单个 key
GET /kv/:prefix?recurse   # 递归读取前缀下所有 key
GET /kv/:prefix?keys      # 只返回 key 列表
GET /kv/:key?raw          # 返回原始值 (text/plain)
```

返回值是 base64 编码，需解码:
```bash
curl -s http://127.0.0.1:8500/v1/kv/my-key | jq -r '.[0].Value' | base64 -d
```

### 写入 KV
```bash
PUT /kv/:key
PUT /kv/:key?flags=123    # 附加 flags
PUT /kv/:key?cas=100      # Check-And-Set (乐观锁)

curl -X PUT -d 'my value' http://127.0.0.1:8500/v1/kv/my-key
```

### 删除 KV
```bash
DELETE /kv/:key           # 删除单个 key
DELETE /kv/:prefix?recurse  # 删除前缀下所有 key
DELETE /kv/:key?cas=100   # Check-And-Set 删除
```

### 分布式锁
```bash
# 获取锁
PUT /kv/:key?acquire=<session-id>

# 释放锁
PUT /kv/:key?release=<session-id>
```

## Health Checks

### 查询节点健康状态
```bash
GET /health/node/:node
```

### 查询服务的健康检查
```bash
GET /health/checks/:service
GET /health/checks/redis?passing  # 只返回 passing 状态
```

### 查询健康的服务实例
```bash
GET /health/service/:service
GET /health/service/redis?passing  # 只返回健康实例
```

### 按状态查询
```bash
GET /health/state/passing
GET /health/state/warning
GET /health/state/critical
GET /health/state/any
```

**健康状态:** `passing`, `warning`, `critical`

## ACL (Access Control)

### 创建 Token
```bash
PUT /acl/create
{
  "Name": "my-token",
  "Type": "client",
  "Rules": "key \"secret/\" { policy = \"read\" }"
}
```

### 列出 Tokens
```bash
GET /acl/list
GET /acl/token/self  # 当前 token 信息
```

### 读取/更新 Token
```bash
GET /acl/token/:accessor_id
PUT /acl/token/:accessor_id
```

## Agent Operations

### 查看 Agent 成员
```bash
GET /agent/members
```

### 查看 Agent 自身信息
```bash
GET /agent/self
```

### 查看本地服务
```bash
GET /agent/services
GET /agent/service/:service_id
```

### 注册服务 (Agent 端点)
```bash
PUT /agent/service/register
{
  "Name": "redis",
  "ID": "redis-1",
  "Tags": ["primary"],
  "Address": "127.0.0.1",
  "Port": 6379,
  "Check": {
    "HTTP": "http://localhost:6379/health",
    "Interval": "10s"
  }
}
```

### 注销服务 (Agent 端点)
```bash
PUT /agent/service/deregister/:service_id
```

## Service Mesh (Connect)

### 查询 Connect 服务
```bash
GET /catalog/connect/:service
GET /health/connect/:service?passing
```

### 查询 Ingress Gateway
```bash
GET /health/ingress/:service
```

### 服务意图 (Intentions)
```bash
GET /connect/intentions
POST /connect/intention
{
  "SourceName": "web",
  "DestinationName": "db",
  "Action": "allow"
}
DELETE /connect/intention/:id
```

## Sessions (分布式锁)

### 创建 Session
```bash
PUT /session/create
{
  "Name": "my-lock",
  "TTL": "30s",
  "Behavior": "delete"
}
```
返回: `{"ID": "session-uuid"}`

### 查询 Session
```bash
GET /session/info/:session-id
GET /session/node/:node
```

### 销毁 Session
```bash
PUT /session/destroy/:session-id
```

## Transactions

原子操作多个 KV 或 Catalog 操作:
```bash
PUT /txn
[
  {"KV": {"Verb": "set", "Key": "key1", "Value": "dGVzdA=="}},
  {"KV": {"Verb": "get", "Key": "key2"}},
  {"Service": {"Verb": "register", "Service": {...}}}
]
```

**支持的 Verb:**
- KV: `set`, `get`, `delete`, `check-index`, `lock`, `unlock`
- Service: `register`, `deregister`

## Blocking Queries

使用 `index` 或 `wait` 实现长轮询:
```bash
# 等待 key 变化
GET /kv/my-key?index=100
GET /kv/my-key?wait=5m&index=100
```

响应头 `X-Consul-Index` 返回当前索引。

## Error Handling

**常见 HTTP 状态码:**
- `200` - 成功
- `404` - 资源不存在
- `400` - 请求格式错误
- `403` - ACL 权限不足
- `500` - 服务器错误

**响应头:**
- `X-Consul-Index` - 当前状态索引
- `X-Consul-KnownLeader` - 是否有已知 leader
- `X-Consul-LastContact` - 最后联系 leader 的时间
- `X-Consul-Default-ACL-Policy` - 默认 ACL 策略

## References

For detailed API specifications, see:
- [api-reference.md](references/api-reference.md) - Complete API endpoint reference