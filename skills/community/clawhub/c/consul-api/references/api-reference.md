# Consul API Reference

完整的 HTTP API 端点参考文档。

## Table of Contents

- [API Structure](#api-structure)
- [Catalog Endpoints](#catalog-endpoints)
- [KV Store Endpoints](#kv-store-endpoints)
- [Health Endpoints](#health-endpoints)
- [Agent Endpoints](#agent-endpoints)
- [ACL Endpoints](#acl-endpoints)
- [Session Endpoints](#session-endpoints)
- [Connect/Service Mesh Endpoints](#connectservice-mesh-endpoints)
- [Transaction Endpoints](#transaction-endpoints)
- [Status Endpoints](#status-endpoints)

---

## API Structure

### Base URL
```
http://127.0.0.1:8500/v1/
```

### Authentication
```bash
# 推荐: X-Consul-Token header
curl -H "X-Consul-Token: <token>" http://127.0.0.1:8500/v1/...

# Bearer token (RFC 6750)
curl -H "Authorization: Bearer <token>" http://127.0.0.1:8500/v1/...
```

### Common Query Parameters
| Parameter | Description |
|-----------|-------------|
| `dc` | Datacenter name |
| `ns` | Namespace (Enterprise) |
| `pretty` | Format JSON output |
| `wait` | Blocking query wait duration |
| `index` | Blocking query index |
| `filter` | Filter expression |

### Blocking Queries
```bash
GET /kv/my-key?index=100
GET /kv/my-key?wait=5m&index=100
```

### Consistency Modes
- `stale` - 允许读取过期数据
- `consistent` - 强一致性读取
- `default` - leader 读取

---

## Catalog Endpoints

### Register Entity
```
PUT /catalog/register
```

**Request Body:**
```json
{
  "Datacenter": "dc1",
  "ID": "40e4a748-2192-161a-0510-9bf59fe950b5",
  "Node": "t2.320",
  "Address": "192.168.10.10",
  "TaggedAddresses": {
    "lan": "192.168.10.10",
    "wan": "10.0.10.10"
  },
  "NodeMeta": {
    "somekey": "somevalue"
  },
  "Service": {
    "ID": "redis1",
    "Service": "redis",
    "Tags": ["primary", "v1"],
    "Address": "127.0.0.1",
    "Port": 8000,
    "Meta": {"redis_version": "4.0"}
  },
  "Check": {
    "Node": "t2.320",
    "CheckID": "service:redis1",
    "Name": "Redis health check",
    "Status": "passing",
    "ServiceID": "redis1"
  }
}
```

### Deregister Entity
```
PUT /catalog/deregister
```

**Request Body:**
```json
// Deregister entire node
{"Node": "t2.320", "Datacenter": "dc1"}

// Deregister a service
{"Node": "t2.320", "ServiceID": "redis1"}

// Deregister a check
{"Node": "t2.320", "CheckID": "service:redis1"}
```

### List Datacenters
```
GET /catalog/datacenters
```

**Response:**
```json
["dc1", "dc2"]
```

### List Nodes
```
GET /catalog/nodes
GET /catalog/nodes?dc=dc1&near=_agent
```

**Response:**
```json
[
  {
    "ID": "40e4a748-2192-161a-0510-9bf59fe950b5",
    "Node": "baz",
    "Address": "10.1.10.11",
    "Datacenter": "dc1",
    "TaggedAddresses": {"lan": "10.1.10.11", "wan": "10.1.10.11"},
    "Meta": {"instance_type": "t2.medium"}
  }
]
```

### List Services
```
GET /catalog/services
GET /catalog/services?dc=dc1&ns=default
```

**Response:**
```json
{
  "consul": [],
  "redis": [],
  "postgresql": ["primary", "secondary"]
}
```

### List Nodes for Service
```
GET /catalog/service/:service_name
GET /catalog/service/web?dc=dc1&ns=default&tag=prod
```

**Response:**
```json
[
  {
    "ID": "40e4a748-2192-161a-0510-9bf59fe950b5",
    "Node": "t2.320",
    "Address": "192.168.10.10",
    "Datacenter": "dc1",
    "ServiceID": "32a2a47f7992:nodea:5000",
    "ServiceName": "web",
    "ServicePort": 5000,
    "ServiceTags": ["prod"],
    "ServiceAddress": "172.17.0.3"
  }
]
```

### List Services for Node
```
GET /catalog/node/:node_name
GET /catalog/node-services/:node_name
```

---

## KV Store Endpoints

### Read Key
```
GET /kv/:key
GET /kv/:key?raw              # Raw value (text/plain)
GET /kv/:prefix?recurse       # Recursive read
GET /kv/:prefix?keys          # Keys only
GET /kv/:prefix?keys&separator=/   # Keys with separator
```

**Metadata Response:**
```json
[
  {
    "CreateIndex": 100,
    "ModifyIndex": 200,
    "LockIndex": 200,
    "Key": "zip",
    "Flags": 0,
    "Value": "dGVzdA==",
    "Session": "adf4238a-882b-9ddc-4a9d-5b6758e4159e"
  }
]
```

**Keys Response:**
```json
["/web/bar", "/web/foo", "/web/subdir/"]
```

### Write Key
```
PUT /kv/:key
PUT /kv/:key?flags=123        # Custom flags
PUT /kv/:key?cas=200          # Check-And-Set
PUT /kv/:key?acquire=<session-id>  # Acquire lock
PUT /kv/:key?release=<session-id>  # Release lock
```

**Request Body:** Raw value (any content)

**Response:** `true` or `false`

### Delete Key
```
DELETE /kv/:key
DELETE /kv/:prefix?recurse    # Delete all with prefix
DELETE /kv/:key?cas=200       # Check-And-Set delete
```

---

## Health Endpoints

### Node Health
```
GET /health/node/:node
```

**Response:**
```json
[
  {
    "Node": "foobar",
    "CheckID": "serfHealth",
    "Name": "Serf Health Status",
    "Status": "passing",
    "ServiceID": "",
    "ServiceName": ""
  }
]
```

### Service Checks
```
GET /health/checks/:service
GET /health/checks/redis?passing
```

### Service Instances
```
GET /health/service/:service
GET /health/service/redis?passing&near=_agent
```

**Response:**
```json
[
  {
    "Node": {
      "ID": "40e4a748-2192-161a-0510-9bf59fe950b5",
      "Node": "foobar",
      "Address": "10.1.10.12"
    },
    "Service": {
      "ID": "redis",
      "Service": "redis",
      "Tags": ["primary"],
      "Address": "10.1.10.12",
      "Port": 8000
    },
    "Checks": [
      {"CheckID": "service:redis", "Status": "passing"}
    ]
  }
]
```

### State Query
```
GET /health/state/:state
```

**States:** `passing`, `warning`, `critical`, `any`

---

## Agent Endpoints

### Members
```
GET /agent/members
```

### Self
```
GET /agent/self
```

### Services
```
GET /agent/services
GET /agent/service/:service_id
```

### Register Service
```
PUT /agent/service/register
```

**Request Body:**
```json
{
  "Name": "redis",
  "ID": "redis-1",
  "Tags": ["primary"],
  "Address": "127.0.0.1",
  "Port": 6379,
  "Check": {
    "HTTP": "http://localhost:6379/health",
    "Interval": "10s",
    "Timeout": "1s"
  },
  "Checks": [...]
}
```

### Deregister Service
```
PUT /agent/service/deregister/:service_id
```

### Checks
```
GET /agent/checks
PUT /agent/check/register
PUT /agent/check/deregister/:check_id
```

### Reload
```
PUT /agent/reload
```

### Maintenance Mode
```
PUT /agent/maintenance?enable=true&reason=upgrade
```

---

## ACL Endpoints

### Bootstrap ACLs
```
PUT /acl/bootstrap
```

### Create Token
```
PUT /acl/create
```

**Request Body:**
```json
{
  "Name": "my-token",
  "Type": "client",  // or "management"
  "Rules": "key \"secret/\" { policy = \"read\" }"
}
```

### List Tokens
```
GET /acl/list
GET /acl/token/self
```

### Token CRUD
```
GET /acl/token/:accessor_id
PUT /acl/token/:accessor_id
DELETE /acl/token/:accessor_id
```

### Policies
```
GET /acl/policies
PUT /acl/policy/:name
GET /acl/policy/:name
DELETE /acl/policy/:name
```

### Roles
```
GET /acl/roles
PUT /acl/role/:name
GET /acl/role/:name
DELETE /acl/role/:name
```

---

## Session Endpoints

### Create Session
```
PUT /session/create
```

**Request Body:**
```json
{
  "Name": "my-lock",
  "Node": "node1",
  "LockDelay": "15s",
  "Behavior": "delete",  // or "release"
  "TTL": "30s"
}
```

**Response:**
```json
{"ID": "adf4238a-882b-9ddc-4a9d-5b6758e4159e"}
```

### Session Info
```
GET /session/info/:session-id
GET /session/node/:node
GET /session/list
```

### Renew Session
```
PUT /session/renew/:session-id
```

### Destroy Session
```
PUT /session/destroy/:session-id
```

---

## Connect/Service Mesh Endpoints

### Connect Services
```
GET /catalog/connect/:service
GET /health/connect/:service?passing
```

### Ingress Gateway
```
GET /health/ingress/:service
```

### Gateway Services
```
GET /catalog/gateway-services/:gateway
```

### Intentions
```
GET /connect/intentions
POST /connect/intention
GET /connect/intention/:id
DELETE /connect/intention/:id
```

**Intention Body:**
```json
{
  "SourceName": "web",
  "DestinationName": "db",
  "Action": "allow"
}
```

### CA
```
GET /connect/ca/roots
GET /connect/ca/configuration
PUT /connect/ca/configuration
```

---

## Transaction Endpoints

```
PUT /txn
```

**Request Body:**
```json
[
  {"KV": {"Verb": "set", "Key": "key1", "Value": "dGVzdA=="}},
  {"KV": {"Verb": "get", "Key": "key2"}},
  {"KV": {"Verb": "delete", "Key": "key3"}},
  {"Service": {"Verb": "register", "Service": {"Service": "redis"}}},
  {"Node": {"Verb": "register", "Node": {...}}}
]
```

**KV Verbs:** `set`, `get`, `delete`, `check-index`, `check-session`, `lock`, `unlock`

**Service Verbs:** `register`, `deregister`

**Node Verbs:** `register`, `deregister`

---

## Status Endpoints

### Leader
```
GET /status/leader
```

**Response:** `"10.1.10.12:8300"`

### Peers
```
GET /status/peers
```

**Response:**
```json
["10.1.10.12:8300", "10.1.10.13:8300"]
```

---

## Filtering

Many list endpoints support filter expressions:

```bash
GET /catalog/nodes?filter=Meta.instance_type == "t2.medium"
GET /health/service/redis?filter=Service.Tags contains "primary"
```

**Supported Operators:**
- `==`, `!=` - Equality
- `in`, `not in` - Membership
- `matches`, `not matches` - Regex
- `contains`, `not contains` - Array membership
- `is empty`, `is not empty` - Empty check

**Example Filters:**
```
Node == "web-1"
ServiceTags contains "production"
Meta.env in ["prod", "staging"]
Address matches "^10\\.1\\..*"
```

---

## Error Responses

**400 Bad Request:**
```json
{"error": "invalid request body"}
```

**403 Forbidden:**
```json
{"error": "Permission denied"}
```

**404 Not Found:**
```json
{"error": "key not found"}
```

**500 Internal Server Error:**
```json
{"error": "internal error"}
```

---

## Response Headers

| Header | Description |
|--------|-------------|
| `X-Consul-Index` | Current state index |
| `X-Consul-KnownLeader` | Has known leader (true/false) |
| `X-Consul-LastContact` | Last leader contact (ms) |
| `X-Consul-Default-ACL-Policy` | Default ACL policy |
| `X-Consul-Results-Filtered-By-ACLs` | Results filtered (true/false) |
| `X-Consul-Translate-Addresses` | Address translation enabled |