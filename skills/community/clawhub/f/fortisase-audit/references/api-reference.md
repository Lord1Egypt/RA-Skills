# FortiSASE REST API Reference

Reference for FortiSASE API endpoints, FortiCloud authentication, and FortiOS
REST API patterns used for thin edge queries. This documents the API
interactions required for programmatic FortiSASE audit operations.

## FortiCloud Authentication

All FortiSASE API calls require a bearer token obtained from the FortiCloud
IAM service. The token is scoped to the FortiCloud account and provides
access to FortiSASE tenant resources based on IAM role assignments.

### Token Request

```
POST https://customerapiauth.fortinet.com/api/v1/oauth/token/
Content-Type: application/json

{
  "username": "<forticloud_username>",
  "password": "<forticloud_password>",
  "client_id": "<api_client_id>",
  "grant_type": "password"
}
```

### Token Response

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "dGhpcyBpcyBhIHJlZnJl..."
}
```

### Token Refresh

```
POST https://customerapiauth.fortinet.com/api/v1/oauth/token/
Content-Type: application/json

{
  "refresh_token": "<refresh_token>",
  "client_id": "<api_client_id>",
  "grant_type": "refresh_token"
}
```

### Authentication Headers

All subsequent API requests must include:

```
Authorization: Bearer <access_token>
Content-Type: application/json
```

### IAM Permission Requirements

| Permission Scope | Required For |
|-----------------|--------------|
| `fortisase:read` | Tenant topology, PoP status, thin edge inventory |
| `fortisase:endpoint:read` | Endpoint compliance, ZTNA tags, FortiClient status |
| `fortisase:policy:read` | Firewall policies, SWG profiles, ZTNA rules |
| `fortisase:logging:read` | Log configuration, alert policies |
| `forticloud:account:read` | License status, subscription details |

## FortiSASE Management API Endpoints

Base URL: `https://<tenant>.fortisase.com/api/v1/fortisase`

### Tenant and Topology

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/pops` | GET | List all Points of Presence with status |
| `/pops/{pop_id}` | GET | Detailed PoP information (capacity, region, health) |
| `/thin-edges` | GET | List all thin edge sites |
| `/thin-edges/{edge_id}` | GET | Detailed thin edge information |
| `/thin-edges/{edge_id}/sdwan/health` | GET | SD-WAN overlay health metrics |
| `/thin-edges/{edge_id}/firmware` | GET | Thin edge firmware version and update status |
| `/license/status` | GET | License utilization and expiration |
| `/endpoints/summary` | GET | Endpoint count summary (connected, total, by platform) |

### Endpoint and Compliance

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/endpoints/compliance` | GET | Compliance summary across all endpoints |
| `/endpoints/ztna-tags` | GET | ZTNA tag assignment inventory |
| `/endpoints/groups` | GET | Endpoint group definitions and membership |
| `/ems/status` | GET | FortiClient EMS integration status |

### Logging and Analytics

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/logging/status` | GET | FortiAnalyzer Cloud connection status |
| `/logging/forwarders` | GET | Log forwarding configuration |
| `/logging/alerts` | GET | Alert policy definitions |

## FortiOS REST API Endpoints (Policy Configuration)

FortiSASE exposes FortiOS CMDB configuration via the standard FortiOS REST
API pattern. These endpoints manage the security policy, UTM profiles, and
inspection settings applied to SWG and ZTNA traffic.

Base URL: `https://<tenant>.fortisase.com/api/v2`

### Firewall Policies

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/cmdb/firewall/policy` | GET | All firewall policies (SWG and ZTNA) |
| `/cmdb/firewall/policy/{policy_id}` | GET | Specific firewall policy detail |
| `/cmdb/firewall/central-snat-map` | GET | Central SNAT policy table |
| `/cmdb/firewall/address` | GET | Address objects used in policies |
| `/cmdb/firewall/addrgrp` | GET | Address groups |
| `/cmdb/firewall/service/custom` | GET | Custom service definitions |
| `/cmdb/firewall/service/group` | GET | Service groups |

### ZTNA Configuration

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/cmdb/firewall/access-proxy` | GET | ZTNA access proxy definitions |
| `/cmdb/firewall/access-proxy/{name}/api-gateway` | GET | ZTNA API gateway rules |
| `/cmdb/firewall/access-proxy/virtual-host` | GET | ZTNA virtual host (server) definitions |
| `/cmdb/user/device-category` | GET | Device categories (posture tags) |
| `/cmdb/user/group` | GET | User group definitions |
| `/cmdb/user/saml` | GET | SAML IdP integration settings |
| `/cmdb/user/ldap` | GET | LDAP server integration settings |

### UTM / Security Profiles

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/cmdb/antivirus/profile` | GET | Antivirus profiles |
| `/cmdb/webfilter/profile` | GET | Web filter profiles |
| `/cmdb/webfilter/ftgd-local-cat` | GET | Local web filter categories |
| `/cmdb/application/list` | GET | Application control lists |
| `/cmdb/ips/sensor` | GET | IPS sensor profiles |
| `/cmdb/ips/rule` | GET | IPS rule definitions |
| `/cmdb/dnsfilter/profile` | GET | DNS filter profiles |
| `/cmdb/videofilter/profile` | GET | Video filter profiles |
| `/cmdb/casb/profile` | GET | Inline CASB profiles |
| `/cmdb/dlp/sensor` | GET | DLP sensor profiles |
| `/cmdb/firewall/ssl-ssh-profile` | GET | SSL/SSH inspection profiles |

### FortiGuard and System Monitoring

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/monitor/system/fortiguard` | GET | FortiGuard signature versions and status |
| `/monitor/fortiguard/service-communication-stats` | GET | FortiGuard service communication statistics |
| `/monitor/fortiguard/server-list` | GET | FortiGuard server list and connectivity |
| `/monitor/system/available-certificates` | GET | Available certificates for SSL inspection |
| `/monitor/license/status` | GET | License feature status |

## Common Response Structures

### Firewall Policy Object

```json
{
  "policyid": 1,
  "name": "SWG-Internet-Access",
  "srcintf": [{"name": "fortisase-swg"}],
  "dstintf": [{"name": "wan"}],
  "srcaddr": [{"name": "all"}],
  "dstaddr": [{"name": "all"}],
  "action": "accept",
  "status": "enable",
  "schedule": "always",
  "service": [{"name": "ALL"}],
  "utm-status": "enable",
  "av-profile": "default",
  "webfilter-profile": "corporate-web-filter",
  "application-list": "corporate-app-control",
  "ips-sensor": "high-security",
  "ssl-ssh-profile": "deep-inspection",
  "logtraffic": "all",
  "comments": "Primary SWG policy for endpoint internet access"
}
```

### Web Filter Profile Object

```json
{
  "name": "corporate-web-filter",
  "comment": "Corporate web filter policy",
  "ftgd-wf": {
    "filters": [
      {
        "id": 1,
        "category": 2,
        "action": "block",
        "log": "enable"
      },
      {
        "id": 2,
        "category": 7,
        "action": "allow",
        "log": "enable"
      }
    ],
    "max-quota-timeout": 300
  },
  "safe-search": "url",
  "safe-search-engine": "enable",
  "youtube-restrict": "strict"
}
```

### ZTNA Access Proxy Object

```json
{
  "name": "ztna-internal-apps",
  "vip": "ztna-vip-internal",
  "client-cert": "enable",
  "auth-portal": "enable",
  "api-gateway": [
    {
      "id": 1,
      "url-map": "/app1",
      "service": "https",
      "realservers": [
        {
          "id": 1,
          "ip": "10.0.1.10",
          "port": 443,
          "status": "active"
        }
      ],
      "persistence": "none",
      "saml-server": "corporate-idp",
      "ztna-tags": [
        {"name": "compliant-device"},
        {"name": "os-patched"}
      ]
    }
  ]
}
```

### Thin Edge Status Object

```json
{
  "edge_id": "FGVM01TM12345678",
  "name": "branch-office-nyc",
  "status": "online",
  "tunnel_status": "up",
  "tunnel_type": "ipsec",
  "pop_connected": "us-east-1",
  "firmware": {
    "current": "7.4.3",
    "recommended": "7.4.4",
    "status": "update_available"
  },
  "sdwan": {
    "status": "active",
    "health_checks": [
      {
        "name": "internet-check",
        "status": "alive",
        "latency": 12.5,
        "jitter": 2.1,
        "packet_loss": 0.0,
        "sla_pass": true
      }
    ]
  },
  "last_seen": "2026-03-22T10:15:00Z"
}
```

### Endpoint Compliance Summary Object

```json
{
  "total_endpoints": 1250,
  "compliant": 1087,
  "non_compliant": 163,
  "compliance_rate": 86.96,
  "breakdown": {
    "os_patch_overdue": 45,
    "av_signatures_stale": 32,
    "critical_vulnerabilities": 18,
    "firewall_disabled": 12,
    "disk_encryption_off": 56
  },
  "ztna_tags": {
    "compliant_device": 1087,
    "non_compliant_device": 163,
    "os_patched": 1205,
    "av_current": 1218
  }
}
```

## FortiOS REST API Patterns for Thin Edge Queries

When querying thin edge FortiGates directly (for policy consistency
verification or detailed device status), the standard FortiOS REST API
pattern applies.

### Direct Thin Edge Authentication

```
# Obtain session token from thin edge FortiGate
POST https://<thin_edge_ip>/api/v2/authentication
Content-Type: application/json

{
  "username": "<admin_user>",
  "secretkey": "<admin_password>"
}
```

Response includes a session cookie or API token for subsequent requests.

### Common Thin Edge Queries

```
# Get thin edge system status
GET https://<thin_edge_ip>/api/v2/monitor/system/status

# Get thin edge firewall policies (for consistency check)
GET https://<thin_edge_ip>/api/v2/cmdb/firewall/policy

# Get thin edge SD-WAN configuration
GET https://<thin_edge_ip>/api/v2/cmdb/system/sdwan

# Get thin edge SD-WAN health check status
GET https://<thin_edge_ip>/api/v2/monitor/system/sdwan/health-check

# Get thin edge VPN tunnel status
GET https://<thin_edge_ip>/api/v2/monitor/vpn/ipsec

# Get thin edge FortiGuard status
GET https://<thin_edge_ip>/api/v2/monitor/system/fortiguard
```

## Pagination

FortiOS REST API responses are paginated for large result sets. Use the
following query parameters:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `count` | Maximum items per page | 500 |
| `start` | Starting index (0-based) | 0 |
| `with_meta` | Include metadata (total count) | false |

Example:
```
GET /api/v2/cmdb/firewall/policy?count=100&start=0&with_meta=true
```

Response metadata:
```json
{
  "http_method": "GET",
  "revision": "abc123",
  "results": [...],
  "vdom": "root",
  "path": "firewall",
  "name": "policy",
  "status": "success",
  "http_status": 200,
  "serial": "FGVM01TM12345678",
  "version": "v7.4.4",
  "build": 2573,
  "matched_count": 42,
  "next_idx": 100,
  "revision_changed": false
}
```

## Rate Limiting

### FortiCloud API

| Limit | Value |
|-------|-------|
| Requests per minute (per token) | 60 |
| Requests per hour (per token) | 1000 |
| Concurrent connections | 10 |
| Rate limit response code | `429 Too Many Requests` |
| Retry header | `Retry-After: <seconds>` |

### FortiOS REST API (Direct Device)

| Limit | Value |
|-------|-------|
| Concurrent admin sessions | 32 (default) |
| API request timeout | 300 seconds |
| Maximum response size | 50 MB |
| Session idle timeout | 900 seconds (configurable) |

### Rate Limit Handling

Implement exponential backoff when receiving `429` responses:

```
Attempt 1: Wait 1 second
Attempt 2: Wait 2 seconds
Attempt 3: Wait 4 seconds
Attempt 4: Wait 8 seconds
Maximum: Wait 60 seconds
```

For audit operations querying many endpoints, batch requests where possible
and maintain a request queue that respects the per-minute rate limit. Use the
`Retry-After` header value when provided rather than a fixed backoff interval.

## Error Response Codes

| HTTP Status | Meaning | Audit Action |
|-------------|---------|--------------|
| `200` | Success | Process response data |
| `400` | Bad request (malformed query) | Fix request syntax |
| `401` | Unauthorized (token expired or invalid) | Refresh token and retry |
| `403` | Forbidden (insufficient permissions) | Verify IAM role assignments |
| `404` | Resource not found | Feature may not be configured; document as N/A |
| `408` | Request timeout | Retry with smaller scope or pagination |
| `429` | Rate limited | Apply exponential backoff; respect Retry-After |
| `500` | Internal server error | Retry after delay; escalate if persistent |
| `503` | Service unavailable | FortiSASE service degradation; check status page |
