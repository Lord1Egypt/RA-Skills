---
name: gateway-watchdog
description: "Monitor OpenClaw Gateway health by detecting abnormal error rates in logs. Use when: (1) setting up Gateway error monitoring, (2) diagnosing repeated API failures (429, quota, timeouts), (3) user asks about Gateway health or error trends, (4) integrating error detection into heartbeat checks. Detects rate-limiting, server errors, auth failures, network errors, and message delivery failures across all channels."
---

# Gateway Watchdog

Detect abnormal error patterns in the OpenClaw Gateway before they cause damage. Works with all channels: Telegram, WhatsApp, Discord, Slack, Signal, iMessage, Feishu, and more.

Born from a real incident: a silent `try-catch` caused 76,744 failed retries in 8 hours — undetected until the API quota was exhausted.

## What It Detects

| Category | Patterns |
|----------|----------|
| Rate limiting | HTTP 429, `rate.limit`, `too many requests` |
| Server errors | HTTP 5xx status codes |
| Auth/permission | HTTP 401/403, `unauthorized`, `forbidden`, `token expired` |
| Network errors | `ETIMEDOUT`, `ECONNREFUSED`, `ECONNRESET`, `ENOTFOUND`, `socket hang up` |
| Delivery failures | `sendMessage failed`, `deliver failed`, `fetch failed` |
| **Custom** | User-defined via `WATCHDOG_EXTRA_PATTERNS` env var |

### Smart Analysis
- **Error rate** (errors/min) — more meaningful than raw count
- **Spike detection** — alerts when errors jump 3x+ vs last check
- **Error concentration** — flags when 80%+ errors are one type (single fault source)

## Quick Start

```bash
bash scripts/gateway-watchdog.sh check     # silent unless errors exceed threshold
bash scripts/gateway-watchdog.sh verbose   # always outputs full report
bash scripts/gateway-watchdog.sh history   # show monitoring history
bash scripts/gateway-watchdog.sh trend     # last 24h error trend
```

### Heartbeat integration

Add to `HEARTBEAT.md`:

```markdown
## Gateway Error Monitoring (every heartbeat)
- Run `~/.openclaw/workspace/skills/gateway-watchdog/scripts/gateway-watchdog.sh check`
- If output is non-empty, report to user immediately
- No output = healthy, skip reporting
```

### Cron (optional)

```bash
openclaw cron add \
  --name "gateway-watchdog" \
  --schedule "*/30 * * * *" \
  --task "Run gateway-watchdog.sh verbose. If errors detected, notify user with the report." \
  --channel last
```

## Configuration

All via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `WATCHDOG_THRESHOLD` | `30` | Error count that triggers alert |
| `WATCHDOG_WINDOW` | `30` | Monitoring window in minutes |
| `WATCHDOG_SPIKE_RATIO` | `3` | Alert when errors jump Nx vs last check |
| `WATCHDOG_EXTRA_PATTERNS` | _(empty)_ | Custom regex patterns (e.g., `99991400\|99991403`) |
| `WATCHDOG_STATE` | `~/.local/state/gateway-watchdog/state.json` | State file |
| `WATCHDOG_LOG` | `~/.local/state/gateway-watchdog/history.log` | History log |

### Adding channel-specific patterns

```bash
# Feishu-specific error codes
export WATCHDOG_EXTRA_PATTERNS='99991400|99991403|99991404|99991429'

# Telegram-specific
export WATCHDOG_EXTRA_PATTERNS='Too Many Requests|FLOOD_WAIT|bot was blocked'

# Discord-specific
export WATCHDOG_EXTRA_PATTERNS='DiscordAPIError|Missing Permissions|Unknown Channel'
```

## Interpreting Results

### 🔴 Alert (Chinese locale)
```
🔴 Gateway 最近 30 分钟出现 150 条异常错误（阈值: 30，5/min）
📈 错误突增: 12 → 150（3倍阈值触发）

错误分类：
  429/限流: 120
  5xx服务端错误: 5
  认证/权限: 0
  网络错误: 5
  消息投递失败: 20

  ⚠️  单一错误类型「429/限流」占比 80%，可能是单一故障源
```

### 🔴 Alert (English equivalent)
```
🔴 Gateway detected 150 errors in the last 30 min (threshold: 30, 5/min)
📈 Error spike: 12 → 150 (3x threshold triggered)

Error breakdown:
  429/Rate-limit: 120
  5xx Server errors: 5
  Auth/Permission: 0
  Network errors: 5
  Delivery failures: 20

  ⚠️  Single error type "429/Rate-limit" accounts for 80%+ — likely a single fault source
```

### 💚 Healthy
No output from `check` mode.

## Limitations

- Requires systemd + journalctl (falls back to `~/.openclaw/logs/` on macOS)
- Reactive, not preventive
- Cannot pinpoint which extension is failing — check error details for clues

## Security

- **Read-only**: Only reads logs
- **No credentials**: No API keys accessed
- **No network**: No outbound requests
- **User state only**: State in `~/.local/state/gateway-watchdog/` (XDG standard, no elevated permissions needed)
