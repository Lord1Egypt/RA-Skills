# Flowtriq API Endpoints Reference

Base URL: `https://flowtriq.com`
All timestamps UTC ISO 8601. All responses JSON.

---

## Authentication

**Node API endpoints** (`/api/v1/agent/*`) require both headers:
```
Authorization: Bearer YOUR_NODE_API_KEY
X-Node-UUID: YOUR_NODE_UUID
```

**Deploy endpoint** (`/api/deploy`) uses a workspace deploy token:
```
Authorization: Bearer YOUR_DEPLOY_TOKEN
```

**Health check** requires no auth.

---

## Platform Health

### GET /api/health
No auth. Returns `{ "status": "ok" }`. Use to check platform reachability.

---

## Deploy API

### POST /api/deploy
Register a new node.

**Headers:** `Authorization: Bearer DEPLOY_TOKEN`

**Body:**
```json
{
  "name": "node-display-name",   // required
  "ip": "203.0.113.10",          // required
  "location": "nyc-1",           // optional
  "os": "Ubuntu 22.04",          // optional
  "interface": "eth0"            // optional, default eth0
}
```

**Response 200:**
```json
{
  "ok": true,
  "node_uuid": "a1b2c3d4-...",
  "api_key": "64-char-hex",
  "name": "node-display-name",
  "ip": "203.0.113.10"
}
```

**Errors:**
- `401` Bad deploy token
- `400` Missing name or IP
- `402` No active subscription
- `409` Node name already exists

---

## Agent API

All endpoints below: `POST/GET https://flowtriq.com/api/v1/agent/{endpoint}`
All require `Authorization` + `X-Node-UUID` headers.

---

### POST /v1/agent/heartbeat
Sent by ftagent every 30 seconds.

**Body:**
```json
{
  "agent_version": "1.2.3",
  "uptime": 86400,
  "os": "Ubuntu 22.04"
}
```

---

### POST /v1/agent/metrics
Sent by ftagent every second with current traffic data.

**Body:**
```json
{
  "pps": 12400,
  "bps": 430000000,
  "tcp_pct": 62.3,
  "udp_pct": 35.1,
  "icmp_pct": 2.6,
  "conn_count": 1840,
  "recorded_at": "2026-03-15T09:44:18Z"
}
```

---

### POST /v1/agent/incident
Opens or updates an active incident.

**Body:**
```json
{
  "attack_family": "syn_flood",
  "severity": "high",
  "peak_pps": 47821,
  "peak_bps": 1700000000,
  "protocol_breakdown": { "tcp": 15.2, "udp": 82.1, "icmp": 2.7 },
  "tcp_flag_breakdown": { "SYN": 1200, "ACK": 400, "RST": 50 },
  "geo_breakdown": { "US": 4200, "CN": 1800, "RU": 920 },
  "source_ip_count": 3241,
  "top_src_ips": [
    { "ip": "1.2.3.4", "count": 5000 }
  ],
  "top_dst_ports": [
    { "port": 80, "count": 12000 }
  ],
  "ioc_matches": ["mirai-variant"],
  "spoofing_detected": true,
  "botnet_detected": true
}
```

**Attack families:** `udp_flood` `syn_flood` `http_flood` `icmp_flood`
`dns_flood` `multi_vector` `unknown`

**Severity levels:** `low` `medium` `high` `critical`

---

### POST /v1/agent/pcap
Upload a PCAP file. Multipart form, max 50 MB.

**Form fields:**
- `incident_id` (integer, required)
- `file` (PCAP file, required)

---

### GET /v1/agent/config
Returns node config, IOC patterns, and pending commands.

**Response 200:**
```json
{
  "node_id": 1,
  "pps_threshold": 50000,
  "baseline": {
    "p99_pps": 12000,
    "mean_pps": 3400
  },
  "ioc_patterns": [
    { "id": 1, "name": "mirai-variant", "protocol": "udp" }
  ],
  "pending_commands": [
    { "id": 5, "command": "iptables -I INPUT -s 1.2.3.4 -j DROP" }
  ]
}
```

---

## Rate Limits

See `https://flowtriq.com/docs?section=rate-limits` for current limits.
Standard node API endpoints are designed for high-frequency agent use and
are not rate-limited for normal agent traffic. Direct API use from external
tooling may be subject to limits.

---

## Error Codes

| Code | Meaning |
|---|---|
| 400 | Bad request, missing or invalid parameters |
| 401 | Invalid or missing API key / deploy token |
| 402 | Payment failed or subscription lapsed |
| 409 | Conflict (e.g. duplicate node name) |
| 500+ | Platform error, check https://flowtriq.com/status |

Full error reference: `https://flowtriq.com/docs?section=errors`
