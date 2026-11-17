# Camoufox Browser — Configuration Guide

> **Skill:** camofox-default-browser · **Version:** 1.1.0
> Server auto-starts with OpenClaw Gateway. Default port **9377**.

---

## 1. Environment Variables

All variables are read at server startup. No restart needed for runtime changes via API (except `CAMOUFOX_EXECUTABLE`).

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CAMOUFOX_EXECUTABLE` | ✅ Yes | *(none)* | Absolute path to the Camoufox binary. Without this, no browser tabs can be created. Typical path: `/root/.cache/camoufox/camoufox`. Verify existence: `test -f "$CAMOUFOX_EXECUTABLE" && echo OK`. |
| `CAMOFOX_API_KEY` | ⚠️ Recommended | *(empty)* | Bearer key used to authorize cookie-import operations (`camofox_import_cookies`). If set, any import request must include this key in the `Authorization` header. Leave empty for permissive mode (not recommended for shared hosting). |
| `CAMOFOX_CRASH_REPORT_ENABLED` | ❌ Optional | `true` | Controls crash telemetry. When `false`, anonymized crash reports (no page content, cookies, or IPs) are suppressed. Set to `false` if you want zero data leaving the host. |
| `PORT` | ❌ Optional | `9377` | TCP port the Camoufox management server binds to. Change only if 9377 is already in use. Must be accessible from OpenClaw's process. |
| `IDLE_TIMEOUT` | ❌ Optional | `300` (5 minutes) | Seconds of inactivity before the browser engine shuts down. Reduces memory footprint during idle periods. Set to `0` to never auto-shutdown. |
| `MAX_TABS` | ❌ Optional | `6` | Maximum concurrent active tabs per session. Each tab consumes ~40–200 MB RAM. Lower values conserve resources; higher values enable more parallel browsing. |

### Example `.env` Snippet

```bash
# File: ~/.openclaw/.env (or wherever OpenClaw reads its env vars)
CAMOUFOX_EXECUTABLE=/root/.cache/camoufox/camoufox
CAMOFOX_API_KEY=cf-api-xxxx-xxxx-xxxx-xxxxxxxxxx
CAMOFOX_CRASH_REPORT_ENABLED=false
PORT=9377
IDLE_TIMEOUT=300
MAX_TABS=6
```

---

## 2. Server Configuration

### Port Binding

The server listens on the port specified by `PORT` (default 9377). The health endpoint is always:

```
GET http://localhost:9377/health
```

Response:

```json
{"status":"ok","browser":"idle"}
{"status":"ok","browser":"active","tabs":2}
```

### Host Binding

By default, the server binds to `localhost` (127.0.0.1). To expose on the network:

```bash
export CAMOUFOX_BIND_HOST=0.0.0.0
```

> ⚠️ **Warning:** Binding to `0.0.0.0` exposes the management API to the network. Combine with firewall rules or reverse proxy authentication. Never expose without TLS in production.

### CORS Settings

Cross-origin requests are allowed from all origins by default (set by OpenClaw gateway routing). For tighter control:

```bash
export CAMOUFOX_CORS_ORIGINS=https://yourdomain.com
```

Set multiple origins as comma-separated values:

```bash
export CAMOUFOX_CORS_ORIGINS=https://a.com,https://b.com
```

An empty value allows all origins (default).

### Rate Limiting

The server applies a basic rate limit of **120 requests per minute** per client IP on management endpoints. Search macros (`@google_search`, etc.) have a separate throttle of **10 searches per minute** to respect target site politeness.

Override defaults:

```bash
export CAMOUFOX_RATE_LIMIT_RPM=60     # requests/minute
export CAMOUFOX_SEARCH_THROTTLE_RPM=5  # searches/minute
```

---

## 3. Browser Configuration

### Fingerprint Settings

Camofox generates a unique fingerprint per session based on real hardware characteristics:

- **WebGL Renderer** — randomized GPU string matching common consumer GPUs
- **AudioContext** — simulated acoustic fingerprints
- **Navigator Properties** — `hardwareConcurrency`, `deviceMemory`, `platform`
- **Screen Geometry** — matched to detected display profile
- **WebRTC** — stable internal IP masking (always uses `127.0.0.1`)
- **Font Enumeration** — cross-platform font subset consistency
- **Canvas Fingerprint** — randomized hash per session

These are managed internally by the C++ engine layer. You do not need to configure individual properties.

### User Agent Customization

The user agent is generated automatically each session. To force a specific string:

```bash
export CAMOUFOX_USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
```

If unset, the server selects a random recent desktop UA from its built-in pool (~200 variants).

### Proxy Support

Route all traffic through a SOCKS5 or HTTP proxy:

```bash
# SOCKS5 proxy
export CAMOUFOX_PROXY=socks5://127.0.0.1:9050

# HTTP proxy
export CAMOUFOX_PROXY=http://proxy.example.com:8080

# Proxy with auth
export CAMOUFOX_PROXY=http://user:pass@proxy.example.com:8080

# No-proxy list (comma-separated hosts)
export CAMOUFOX_PROXY_NO=localhost,127.0.0.1,.internal.local
```

Individual tab navigation respects these settings globally. Per-tab proxy override is available via the `evaluate` tool injecting `pref()` calls.

### Cookie Persistence

Cookies are stored in an ephemeral profile directory that persists while the browser is running. On idle shutdown, the profile is destroyed (no residual data).

For persistent authenticated sessions, use `camofox_import_cookies` with a Netscape-format `cookies.txt`:

```bash
# Import cookies for a specific domain
curl -X POST http://localhost:9377/api/import-cookies \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $CAMOFOX_API_KEY" \
  -d '{"cookiesPath":"/path/to/cookies.txt","domainSuffix":"instagram.com"}'
```

> 🔒 Treat imported cookie files as live credentials. They grant full account access equivalent to being logged in.

---

## 4. Performance Tuning

### Memory Limits

Typical resource usage:

| State | Memory | Notes |
|-------|--------|-------|
| Idle (no browser) | ~5 MB | Server process only |
| Browser launched (no tabs) | ~40 MB | Engine loaded, first tab pending |
| 1 active tab | ~120–200 MB | Depends on page complexity |
| Max tabs (6 × 200 MB) | ~1.2 GB | Upper bound under heavy load |

Control memory via `MAX_TABS`. Lower values reduce peak RSS but increase wait time when many tabs are needed simultaneously.

### Tab Pooling

Camoufox does not pre-create tabs. Tabs are lazily allocated on `create_tab`. To simulate pooling behavior:

```bash
# Keep 2 warm tabs ready
export IDLE_TIMEOUT=0        # disable shutdown
export MAX_TABS=6
```

Then manually create tabs and keep them alive. This trades memory for reduced creation latency (~2–3 seconds per new tab).

### Lazy Loading Settings

The browser engine starts only on the first tab request. Cold start takes approximately **3–5 seconds**:

```
Request → Engine Launch → Profile Init → Ready ≈ 3-5s
```

Subsequent tab creation within the same session is nearly instant (< 500 ms) since the engine is already running.

Optimize cold starts by setting a shorter `IDLE_TIMEOUT` so the engine stays warm during active work hours.

---

## 5. Security Configuration

### API Key Requirements

When `CAMOFOX_API_KEY` is set, these operations require the `Authorization: Bearer <key>` header:

| Operation | Key Required | Risk Level |
|-----------|-------------|------------|
| `import_cookies` | ✅ Mandatory | 🔴 Critical |
| `evaluate` (JS execution) | ✅ Recommended | 🟡 High |
| `navigate` | ❌ Not required | 🟢 Low |
| `click` / `type` | ❌ Not required | 🟢 Low |
| `snapshot` / `screenshot` | ❌ Not required | 🟢 Low |
| Health/status endpoints | ❌ Never required | ℹ️ Info |

Best practice: always set `CAMOFOX_API_KEY` and never share it across environments.

### Access Control

| Layer | Control |
|-------|---------|
| Network | Bind host (`localhost` vs `0.0.0.0`) + firewall rules |
| Authentication | API key bearer token for sensitive operations |
| Origin | CORS origin whitelist via `CAMOUFOX_CORS_ORIGINS` |
| Rate limit | Per-IP request throttling (configurable) |

There is no role-based access control — the API treats all authenticated requests equally. Implement your own RBW at the reverse-proxy level if needed.

### Telemetry Settings

Crash telemetry collects:

- Timestamp and severity level
- Crash type (segfault, OOM, unhandled exception)
- Browser version and OS info
- Number of open tabs at crash time

**Explicitly excluded:**

- Page URLs or content
- Cookies or authentication tokens
- Input text typed into forms
- Client IP addresses
- Screenshot data

Control with:

```bash
# Disable entirely
CAMOFOX_CRASH_REPORT_ENABLED=false

# Enable (default)
CAMOFOX_CRASH_REPORT_ENABLED=true
```

Telemetry data, when enabled, is sent to the Camoufox project's anonymous reporting endpoint for crash analytics only.

---

## Quick Reference Card

```yaml
# Minimal viable config (just get it running)
CAMOUFOX_EXECUTABLE: /root/.cache/camoufox/camoufox

# Production-hardened config
CAMOUFOX_EXECUTABLE: /root/.cache/camoufox/camoufox
CAMOFOX_API_KEY: cf-api-rotate-me-quarterly
CAMOUFOX_CRASH_REPORT_ENABLED: false
PORT: 9377
IDLE_TIMEOUT: 600          # 10 min idle before shutdown
MAX_TABS: 4                # conservative for 8GB host
CAMOUFOX_BIND_HOST: localhost   # never 0.0.0.0 without TLS
CAMOUFOX_CORS_ORIGINS: ""      # allow all (gateway handles routing)
```
