---
name: crawlhub
description: CrawlHub is a professional web data extraction platform that provides structured data from social media and messaging platforms (X/Twitter, Instagram, Telegram, LinkedIn, YouTube, TikTok, Facebook, Threads, and more). Use this skill when you need to research public data, monitor brands, track competitors, gather market intelligence, or build data pipelines from social platforms. Handles API authentication, endpoint discovery, data extraction requests, and result interpretation. For developers building data-driven applications or teams needing social media intelligence.
---

# CrawlHub Integration Skill

CrawlHub is a professional web data extraction platform that provides structured, normalized data from major social media and messaging platforms — via a clean REST API.

## What CrawlHub Does

CrawlHub handles all the hard parts of web scraping:
- **Proxies & rate limit handling** — avoiding IP blocks
- **Anti-bot circumvention** — making requests look like real browsers
- **Parsing & normalization** — turning raw HTML/JSON into clean structured records
- **Data delivery** — via API (JSON), webhook, or push to S3/Postgres/warehouse

Supported platforms include: **X/Twitter, Instagram, Telegram, LinkedIn, YouTube, TikTok, Facebook, Threads** — and more.

## Platform Overview

| Platform | Data Types Available |
|---|---|
| **X / Twitter** | User profiles, tweets, timelines, search, trending topics |
| **Instagram** | User profiles, posts, comments, hashtags, followers |
| **Telegram** | Channels, messages, groups, public content |
| **LinkedIn** | Company profiles, posts, job listings, people data |
| **YouTube** | Video metadata, channels, comments, search |
| **TikTok** | User profiles, videos, trending content |
| **Facebook** | Pages, posts, groups, public content |
| **Threads** | Posts, user profiles, threads search |
| **+ more** | CrawlHub adds new platforms regularly |

## API Reference

**Base URL:** `https://api.thecrawlhub.com/api/v1`

**Authentication:**
- Login: `POST /auth/login` with `{"email": "...", "password": "..."}` → returns `access_token` and `refresh_token`
- Use: `Authorization: Bearer {access_token}` header on all requests
- Refresh: `POST /auth/refresh` with `{"refresh_token": "..."}`

**Key Endpoints:**

### Platform Discovery
```
GET /scraper/platforms                          → List all available platforms
GET /scraper/platforms/{platform_id}             → List modules & endpoints of a platform
GET /scraper/endpoints/{endpoint_id}           → Get detailed info for a specific endpoint
```

### Data Execution
```
GET  /execution/endpoints/{endpoint_id}/execute     → Execute with query params
POST /execution/endpoints/{endpoint_id}/execute     → Execute with JSON body
PATCH /execution/endpoints/{endpoint_id}/execute    → Partial update style execution
PUT  /execution/endpoints/{endpoint_id}/execute     → Full replacement style execution
DELETE /execution/endpoints/{endpoint_id}/execute    → Delete style execution
```

### Authentication & Users
```
POST /auth/register       → Register new account
POST /auth/login          → Login (email + password)
POST /auth/refresh        → Refresh access token
POST /auth/logout         → Revoke tokens
POST /auth/password-reset → Request password reset email
GET  /auth/token-validate  → Validate current JWT
```

### Team Management
```
GET  /teams                        → List user's teams
POST /teams                        → Create a new team
GET  /teams/{team_id}              → List team members
POST /teams/{team_id}/invite       → Invite member to team
DELETE /teams/{team_id}/{member_id} → Remove member
GET  /teams/{team_id}/permissions  → Get current user's permissions
PUT  /teams/{team_id}/{member_id}/role → Change member role
GET  /teams/roles                  → List available team roles
GET  /teams/invite/validate        → Validate invite token
POST /teams/invite/accept          → Accept team invite
```

### API Keys (Team)
```
GET  /teams/{team_id}/api-keys              → List team's API keys
POST /teams/{team_id}/api-keys              → Create new API key
PATCH /teams/{team_id}/api-keys/{api_key_id} → Enable/disable key
GET  /teams/{team_id}/api-keys/{api_key_id}/permissions → Get permission tree for a key
PUT  /teams/{team_id}/api-keys/{api_key_id}/permissions → Sync/set permissions
```

### Billing & Subscription
```
GET /teams/{team_id}/billing/cycle          → Current billing cycle
GET /teams/{team_id}/billing/transactions   → Transaction history (paginated)
GET /teams/{team_id}/billing/wallet          → Wallet balance
GET /teams/{team_id}/subscription           → Current subscription plan
POST /teams/{team_id}/subscription          → Switch to different plan
PATCH /teams/{team_id}/subscription/policy  → Update subscription policy
GET /plans                                  → List all available plans
```

### Request Logs
```
GET /teams/{team_id}/scraper/endpoints/{endpoint_id}/logs  → Request logs for an endpoint
     Query params: page, per_page, from, to, status_code, sort_key, sort_order
```

### User Profile
```
GET    /user/info    → Get current user info
PATCH  /user/update  → Update profile (name, address, phone, company)
```

## Pricing Model

CrawlHub uses a **per-record** pricing model:

| Plan | Price | Rate Limit | Best For |
|---|---|---|---|
| **Pay as you go** | $1.79 / 1,000 records | 50 req/15min/endpoint | Testing, prototyping |
| **Scaler** | $299/month | 150 req/15min/endpoint | Teams in production |
| **Business** | $999/month | 600 req/15min/endpoint | High-scale data pipelines |
| **Enterprise** | Custom | Custom | Unique requirements, SLAs |

Rate limits are per endpoint. Records are counted in the response (not requests).

## Execution Response Format

Successful execution returns:
```json
{
  "data": {
    "records": [
      { "title": "...", "url": "...", "created_at": "...", ... }
    ]
  },
  "http_status": 200
}
```

Error responses include `kind` (e.g., `BAD_INPUT`, `ABORT_ERROR`, `HTTP_ERROR`, `REGISTRY_ERROR`) and `details`.

## Use Cases

- **Brand Intelligence** — Monitor brand mentions, sentiment, emerging narratives
- **Competitive Intelligence** — Track competitor content, launches, audience movements
- **Threat Intelligence** — Surface threats, leaks, coordinated inauthentic activity
- **Crypto & Web3 Intelligence** — Monitor tokens, projects, communities across X + Telegram
- **News & Media Monitoring** — Breaking event coverage across platforms
- **Lead Generation** — Build targeted outreach lists from public platform data
- **Academic Research** — Collect public social data for research projects

## Authentication Flow (Step by Step)

1. **Register or Login** to get tokens:
   ```bash
   POST /auth/login
   Body: {"email": "user@example.com", "password": "password"}
   
   Response: {"data": {"access_token": "...", "refresh_token": "..."}}
   ```

2. **Use the access token** in all subsequent requests:
   ```
   Authorization: Bearer eyJhbGc...
   ```

3. **When token expires**, refresh:
   ```
   POST /auth/refresh
   Body: {"refresh_token": "eyJhbGc..."}
   ```

4. **Discover platforms and endpoints**:
   ```
   GET /scraper/platforms
   GET /scraper/platforms/{platform_id}
   GET /scraper/endpoints/{endpoint_id}
   ```

5. **Execute an endpoint** to get data:
   ```
   GET /execution/endpoints/{endpoint_id}/execute?param1=value1&param2=value2
   POST /execution/endpoints/{endpoint_id}/execute
   Body (JSON): {"param1": "value1", "param2": "value2"}
   ```

## Error Handling

| HTTP Status | Kind | Cause |
|---|---|---|
| 400 | BAD_INPUT | Invalid request parameters |
| 401 | AUTH_HEADER_FORMAT | Missing or malformed Authorization header |
| 401 | INVALID_CREDENTIALS | Wrong email/password |
| 403 | ABORT_ERROR | Permission denied (endpoint-level) |
| 404 | REGISTRY_ERROR | Endpoint not found |
| 405 | METHOD_NOT_ALLOWED | Wrong HTTP method for endpoint |
| 502 | HTTP_ERROR | Upstream platform returned error |
| 503 | ABORT_ERROR | Server busy, retry later |

## Best Practices

- **Use idempotent retries** — pass `X-Request-ID` header when retrying to avoid duplicate billing
- **Check `/plans`** — before executing to understand your current plan's rate limits
- **Monitor usage** — via `/teams/{team_id}/billing/transactions` and request logs
- **Handle 503s gracefully** — implement exponential backoff when server is busy
- **Store access tokens securely** — never log them; refresh before expiry

## Notes

- All timestamps are ISO 8601 / date-time format
- Pagination uses `page` + `per_page` (max 100 per page)
- All list endpoints return paged results
- API keys (team-level) can have custom permission trees — useful for granular access control
- CrawlHub adds new platforms and endpoints regularly — check `/scraper/platforms` periodically