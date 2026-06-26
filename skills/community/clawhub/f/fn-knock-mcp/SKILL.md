---
name: fn-knock-mcp
description: Manage fn-knock gateway via its admin API — reverse proxy, DDNS, SSL/ACME, tunnels (FRP/Cloudflared), scanner, whitelist, and more. Requires fn-knock running on localhost:7998.
metadata: {"openclaw":{"emoji":"🌐","requires":{"anyBins":["python3"]},"os":["linux"]}}
---

## What is fn-knock?

fn-knock is a self-hosted gateway/reverse proxy solution for NAS and home lab environments.
This MCP Server exposes its admin API (100+ endpoints) as structured tools for AI assistants.

## Installation

### 1. Install the MCP package

```bash
pip install mcp requests
# or with uv
uv tool install fn-knock-mcp  # (if published to PyPI)
```

If installing from source:
```bash
cd fn_knock_mcp
pip install -e .
```

### 2. Configure HMAC Secret (3 ways, pick one)

fn-knock's admin API requires HMAC authentication. The MCP auto-resolves the secret using this priority:

**方式 A — 环境变量（推荐）**
```bash
export FN_KNOCK_HMAC_SECRET="your-secret-here"
```

**方式 B — 凭证文件**
```bash
mkdir -p ~/.config/fn-knock
echo "HMAC_SECRET=your-secret-here" > ~/.config/fn-knock/credentials
chmod 600 ~/.config/fn-knock/credentials
```

**方式 C — 自动检测（仅限本地运行 fn-knock）**
如果 fn-knock 正在本机运行（http://localhost:7998），MCP 会自动从页面 HTML 中提取密钥，无需额外配置。

### 3. Add to OpenClaw MCP Settings

Edit your `~/.openclaw/openclaw.json` (or use the OpenClaw web UI):

```json
{
  "mcpServers": {
    "fn-knock": {
      "command": "python",
      "args": ["-m", "fn_knock_mcp.server"],
      "env": {
        "FN_KNOCK_BASE_URL": "http://localhost:7998/api/admin"
      }
    }
  }
}
```

Or reference the provided `mcp.json`:
```json
{
  "mcpServers": {
    "fn-knock": {
      "command": "python",
      "args": ["-m", "fn_knock_mcp.server"]
    }
  }
}
```

> **Note**: The HMAC secret is resolved at startup via env file or auto-detection — do NOT put it in mcp.json.

### 4. (Optional) Configure HTTP Proxy

If fn-knock needs to reach external services (GitHub API, DNS providers, etc.) and you're behind a proxy:

```bash
export HTTP_PROXY=http://192.168.31.21:7890
export HTTPS_PROXY=http://192.168.31.21:7890
```

## Available Tools (58 total)

### Dashboard
- `fnknock_dashboard_stats` — Traffic/auth/threat stats (configurable time range)
- `fnknock_realtime_traffic` — Current real-time bytes in/out

### Config & Run Mode
- `fnknock_get_config` — Full gateway config
- `fnknock_update_run_type` — Switch mode: direct / reverse_proxy / subdomain_proxy / tunnel
- `fnknock_sync_routes` — Trigger immediate route reload

### Reverse Proxy (Host Mappings)
- `fnknock_get_host_mappings` — List all host → target rules
- `fnknock_add_host_mapping` — Add a reverse proxy rule
- `fnknock_delete_host_mapping` — Remove a rule by host

### Stream / Tunnel
- `fnknock_get_stream_mappings` — List port mappings
- `fnknock_update_stream_mappings` — Replace all stream mappings
- `fnknock_frp_status` / `frp_start` / `frp_stop` — FRP tunnel control
- `fnknock_cloudflared_status` / `cloudflared_start` / `cloudflared_stop`

### SSL / ACME
- `fnknock_ssl_status` — Certificate library status
- `fnknock_acme_overview` — ACME jobs & applications
- `fnknock_acme_dns_providers` — Supported DNS providers
- `fnknock_acme_create_application` — Create and submit a cert request

### DDNS
- `fnknock_ddns_status` — Current DDNS state and last IP
- `fnknock_ddns_toggle` — Enable/disable DDNS
- `fnknock_ddns_save_config` — Save provider config
- `fnknock_ddns_test` — Test connectivity and detect public IP

### Auth & Security
- `fnknock_get_auth_settings` — Auth settings (session timeout, 2FA)
- `fnknock_get_totp_status` — TOTP 2FA status
- `fnknock_totp_setup` — Initiate TOTP enrollment
- `fnknock_totp_bind` — Complete TOTP binding
- `fnknock_passkey_list` — List registered passkeys

### IP Management
- `fnknock_whitelist_list` / `whitelist_add` / `whitelist_delete`
- `fnknock_ip_lookup` — Batch IP geolocation lookup (up to 20 IPs)

### Scanner / Security
- `fnknock_scanner_settings` — Path scanner config
- `fnknock_scanner_blacklist` — Blocked suspicious IPs
- `fnknock_scanner_toggle` — Enable/disable scanner protection

### Logs & Events
- `fnknock_get_events` — System event log (filterable)
- `fnknock_delete_events` — Delete events by ID
- `fnknock_gateway_logs_dates` — Dates with gateway logs
- `fnknock_gateway_logs_entries` — Access logs for a date

### Notifications
- `fnknock_notifications_providers` — Notification channels
- `fnknock_notifications_rules` — Notification rules
- `fnknock_notifications_triggers` — Historical notification trigger records (可按 status/rule_id 筛选)
- `fnknock_notifications_deliveries` — Historical delivery records (可按 status/provider_id/rule_id/trigger_id 筛选)
- `fnknock_notifications_deliveries_clear` — Clear delivery records (不传参数则清空全部)

### Gateway & Network
- `fnknock_gateway_settings` / `gateway_update`
- `fnknock_gateway_visibility` — Regional visibility config
- `fnknock_system_reset_firewall` — Reset firewall for a run type
- `fnknock_system_dnsmasq_status` — DNS proxy status

### Sessions & Terminal
- `fnknock_sessions_list` — Active user sessions
- `fnknock_session_kick` — Kick a session
- `fnknock_terminal_status` / `terminal_sessions` — tmux management
- `fnknock_backoff_list` / `backoff_reset` — Rate limit state

### Maintenance
- `fnknock_backup_export` / `backup_import`
- `fnknock_update_check` — Check for fn-knock updates
- `fnknock_traffic_stats` — Traffic statistics

## Finding Your HMAC Secret

If fn-knock is running, open its web UI at http://localhost:7998 and check:
- Browser DevTools → Network tab → any API request → look for `x-timestamp`, `x-nonce`, `x-signature` headers
- Or search the page source for `__FN_KNOCK_HMAC_SECRET__`

The secret is a 64-char hex string. Create the credentials file with it:
```bash
mkdir -p ~/.config/fn-knock
echo "HMAC_SECRET=42e0a9e578284ad8313752293a3079680b377c249e0e3306527442b363a4cd78" \
  > ~/.config/fn-knock/credentials
```

## Troubleshooting

**"Missing Required Security Headers"**
→ HMAC secret is wrong or not resolved. Check env var or credentials file.

**"Request Expired or Time Desynced"**
→ System clock is out of sync. Run `timedatectl set-ntp true` on Linux.

**MCP not loading in OpenClaw**
→ Verify Python path: `which python` and confirm `mcp` package is installed there.
→ Check OpenClaw logs: `openclaw logs` for MCP initialization errors.

**Port 7998 unreachable**
→ fn-knock may be bound to a different interface. Check its listen address in the config.
