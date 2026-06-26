# Service Management API Reference

Default base URL: `https://aicadegalaxy.com/agent`

Confirm this default with the user the first time the skill is used. If they provide another base URL, reuse that confirmed URL for the rest of the session.

This skill covers:

1. Register/update service: `POST /admin/gateway/services`
2. Query service detail: `GET /admin/gateway/services/{serviceId}`
3. Disable service: `PATCH /admin/gateway/services/{serviceId}/status?enabled=false`

## Signed Authentication

All service-management requests require API key signature authentication.

Required headers:

```http
X-API-Key: ${AICADE_API_KEY}
X-Client-Time: 1710000000
X-Nonce: random-uuid
X-Signature: hmac_sha256_hex
X-Content-MD5: body_md5_hex
```

Environment values:

- `AICADE_API_KEY`
- `AICADE_API_SECRET_KEY`

`SECRET_KEY` may be accepted as a compatibility alias for `AICADE_API_SECRET_KEY`.

### Signature Source

Build the signature source with newline separators:

```text
METHOD
PATH
QUERY
X-Client-Time
X-Nonce
BODY_MD5
```

Examples:

```text
POST
/admin/gateway/services

1710000000
random-uuid
body_md5_hex
```

```text
PATCH
/admin/gateway/services/my-service/status
enabled=false
1710000000
random-uuid
d41d8cd98f00b204e9800998ecf8427e
```

Algorithm:

```text
HMAC_SHA256(signatureSource, AICADE_API_SECRET_KEY)
```

The result must be lowercase hex.

## Register Or Update Service

| Field | Value |
| --- | --- |
| Method | `POST` |
| Path | `/admin/gateway/services` |
| Content-Type | `application/json` |
| Behavior | Registers a new gateway service, billing config, rate limits, and refreshes routes |

### Request Body Fields

Use camelCase fields:

| Field | Required | Notes |
| --- | --- | --- |
| `serviceId` | Yes | Lowercase letters, digits, hyphens only |
| `serviceName` | Yes | Display name |
| `endpointUrl` | Yes | Upstream URL, starts with `http://` or `https://` |
| `requestMethod` | No | Upstream method such as `GET` or `POST` |
| `authType` | Yes | `NONE`, `API_KEY`, `BEARER_TOKEN`, `BASIC_AUTH`, `OAUTH2` |
| `authLocation` | No | `HEADER` or `QUERY` |
| `outboundAuth` | Conditional | Required when `authType` is not `NONE` |
| `routePath` | Yes | Gateway route path, must start with `/`; normalize if user omits slash |
| `stripPrefix` | No | Default `0`, range `0-10` |
| `routeOrder` | No | Default `0` |
| `timeoutMs` | No | Default `30000`, range `1000-300000` |
| `enabled` | No | Boolean |
| `description` | No | Service description |
| `tags` | No | Array of strings |
| `inputSchema` | Yes | JSON Schema-compatible input contract |
| `outputSchema` | Yes | JSON Schema-compatible output contract |
| `billing` | Yes | Billing config |
| `rateLimits` | No | Rate limit rules |

### Billing

Common fields:

- `billingType`: `FREE`, `PER_REQUEST`, `PER_TOKEN`, `SUBSCRIPTION`
- `flowType`: usually `INCOME`
- `currency`: such as `POINTS` or `AGS`
- `pricePerRequest`: for `PER_REQUEST`
- `promptPricePer1k`, `completionPricePer1k`: for `PER_TOKEN`
- `subscriptionPeriod`, `subscriptionPrice`: for `SUBSCRIPTION`
- `fallbackStrategy`: such as `REJECT`, `OVERDRAFT`, `DEGRADE`

### Rate Limits

Common fields:

- `limitDimension`: `SERVICE`, `USER`, `IP`
- `qps`
- `rpm`
- `rpd`
- `maxTokensPerReq`
- `ipWhitelist`
- `ipBlacklist`

### Register Example

See `assets/register-service.example.json`.

Success response:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "serviceId": "openai-gpt4",
    "serviceName": "OpenAI GPT-4",
    "endpointUrl": "https://api.openai.com",
    "enabled": true
  }
}
```

## Query Service Detail

| Field | Value |
| --- | --- |
| Method | `GET` |
| Path | `/admin/gateway/services/{serviceId}` |
| Body | Empty |

`BODY_MD5` for signature is the empty-body MD5:

```text
d41d8cd98f00b204e9800998ecf8427e
```

Success response:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "serviceId": "openai-gpt4",
    "serviceName": "OpenAI GPT-4",
    "endpointUrl": "https://api.openai.com",
    "enabled": true,
    "billing": {},
    "rateLimits": []
  }
}
```

## Disable Service

Disable uses the service status endpoint:

| Field | Value |
| --- | --- |
| Method | `PATCH` |
| Path | `/admin/gateway/services/{serviceId}/status` |
| Query | `enabled=false` |
| Body | Empty |

Do not ask for or send operator headers.

Success response:

```json
{
  "code": 200,
  "message": "success"
}
```

## Error Handling

| Status | Meaning | Action |
| --- | --- | --- |
| `401` | API key or signature error | Check `AICADE_API_KEY`, `AICADE_API_SECRET_KEY`, timestamp, nonce, signature path, query, and body MD5 |
| `422` | Validation failed | Check request JSON fields and naming |

Do not interpret `401` as an invalid service JSON, missing `serviceId`, route mismatch, billing error, or schema error.
