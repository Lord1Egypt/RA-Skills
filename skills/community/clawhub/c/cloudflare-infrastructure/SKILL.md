---
name: cloudflare-infrastructure
description: Manage Cloudflare zones, DNS records, workers, rules, firewall settings, and account resources via the Cloudflare API. Use this skill when users want to inspect DNS records, manage zones, configure workers, or update firewall rules.
---

# Cloudflare

![Cloudflare](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/cloudflare.svg?v=2)

Work with Cloudflare from chat — manage zones, DNS records, workers, rules, firewall settings, and account resources via the Cloudflare API with API token authentication.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=cloudflare-infrastructure) for hosted connection flows and credentials so you do not need to configure Cloudflare API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Cloudflare |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Cloudflare |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Cloudflare API    │
│   (User Chat)   │     │   (API Token)│     │ (Zones/DNS/APIs) │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Cloudflare│                       │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ Cloudflare│
   │  File    │           │ Auth     │           │ Dashboard│
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Cloudflare again."

## Quick Start

```bash
# List all zones
clawlink_call_tool --tool "cloudflare_list_zones" --params '{}'

# List DNS records in a zone
clawlink_call_tool --tool "cloudflare_list_dns_records" --params '{"zone_id": "ZONE_ID"}'

# List accounts
clawlink_call_tool --tool "cloudflare_list_accounts" --params '{}'
```

## Authentication

All Cloudflare tool calls are authenticated automatically by ClawLink using the user's connected Cloudflare account.

**No API token is required in chat.** ClawLink stores the API token securely and injects it into every Cloudflare API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=cloudflare and connect Cloudflare.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `cloudflare` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration cloudflare
```

**Response:** Returns the live tool catalog for Cloudflare.

### Reconnect

If Cloudflare tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=cloudflare
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration cloudflare`

## Security & Permissions

- Access is scoped to the permissions granted by the Cloudflare API token.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete zone, delete DNS record, delete WAF list) are marked as high-impact and must be confirmed.

## Tool Reference

### Zones

| Tool | Description | Mode |
|------|-------------|------|
| `cloudflare_list_zones` | List zones in the account with pagination | Read |
| `cloudflare_create_zone` | Create a new DNS zone (domain) | Write |
| `cloudflare_update_zone` | Update zone properties (one field at a time) | Write |
| `cloudflare_delete_zone` | Permanently delete a zone and all DNS records | Write |

### DNS Records

| Tool | Description | Mode |
|------|-------------|------|
| `cloudflare_list_dns_records` | List and search DNS records in a zone | Read |
| `cloudflare_create_dns_record` | Create a new DNS record in a zone | Write |
| `cloudflare_update_dns_record` | Update an existing DNS record | Write |
| `cloudflare_delete_dns_record` | Permanently delete a DNS record | Write |

### Accounts & Members

| Tool | Description | Mode |
|------|-------------|------|
| `cloudflare_list_accounts` | List all Cloudflare accounts accessible to the user | Read |
| `cloudflare_list_account_members` | List account members with roles and permissions | Read |

### Load Balancers

| Tool | Description | Mode |
|------|-------------|------|
| `cloudflare_list_monitors` | List load balancer monitors | Read |
| `cloudflare_list_pools` | List load balancer origin pools | Read |

### WAF & Rules

| Tool | Description | Mode |
|------|-------------|------|
| `cloudflare_list_firewall_rules` | List firewall rules for a zone | Read |
| `cloudflare_create_list` | Create a WAF custom list (IPs, hostnames, ASNs) | Write |
| `cloudflare_get_lists` | List all WAF lists | Read |
| `cloudflare_update_list` | Update a WAF list description | Write |
| `cloudflare_delete_list` | Delete a WAF list | Write |

### Tunnels

| Tool | Description | Mode |
|------|-------------|------|
| `cloudflare_list_tunnels` | List Cloudflare Tunnel tunnels | Read |
| `cloudflare_update_tunnel_configuration` | Update tunnel ingress rules (replaces full config) | Write |

### Bot Management

| Tool | Description | Mode |
|------|-------------|------|
| `cloudflare_get_bot_management_settings` | Get bot management configuration for a zone | Read |

## Code Examples

### List zones

```bash
clawlink_call_tool --tool "cloudflare_list_zones" \
  --params '{}'
```

### Create a DNS record

```bash
clawlink_call_tool --tool "cloudflare_create_dns_record" \
  --params '{
    "zone_id": "ZONE_ID",
    "type": "A",
    "name": "api",
    "content": "192.0.2.1",
    "ttl": 3600
  }'
```

### Update a DNS record

```bash
clawlink_call_tool --tool "cloudflare_update_dns_record" \
  --params '{
    "zone_id": "ZONE_ID",
    "dns_record_id": "RECORD_ID",
    "type": "A",
    "name": "api",
    "content": "192.0.2.2",
    "ttl": 1800
  }'
```

### Delete a DNS record

```bash
clawlink_call_tool --tool "cloudflare_delete_dns_record" \
  --params '{
    "zone_id": "ZONE_ID",
    "dns_record_id": "RECORD_ID"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Cloudflare is connected.
2. Call `clawlink_list_tools --integration cloudflare` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `cloudflare`.
5. If no Cloudflare tools appear, direct the user to https://claw-link.dev/dashboard?add=cloudflare.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → describe → call                              │
│                                                             │
│  Example: List zones → List DNS records → Show results      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                     │
│  list → get → describe → preview → confirm → call         │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute update                                 │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Zone IDs and DNS record IDs are required for all zone-scoped operations — retrieve them via list tools first.
- Pagination: use `page` and `per_page` parameters and check `result_info.total_pages` to iterate all pages.
- Tunnel configuration updates replace the entire configuration — fetch the current config first to avoid losing existing rules.
- WAF lists have plan-based limits (Free: 1 list, Pro/Business: 10 lists, Enterprise: 1000 lists).
- DNS record updates only modify provided fields.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration cloudflare`. |
| Missing connection | Cloudflare is not connected. Direct the user to https://claw-link.dev/dashboard?add=cloudflare. |
| `zone_not_found` | Zone does not exist or is not accessible. |
| `dns_record_not_found` | DNS record does not exist. |
| `InvalidArgument` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `cloudflare`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Cloudflare API Documentation](https://developers.cloudflare.com/api/)
- [Cloudflare DNS API](https://developers.cloudflare.com/api/operations/dns-records-for-a-zone)
- [Cloudflare Zones API](https://developers.cloudflare.com/api/operations/zones)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=cloudflare-infrastructure
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [AWS](https://clawhub.ai/hith3sh/aws-infrastructure) — For AWS infrastructure management
- [GitHub](https://clawhub.ai/hith3sh/github-repos) — For GitHub CI/CD and deployments
- [Datadog](https://clawhub.ai/hith3sh/datadog-monitoring) — For observability and monitoring

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=cloudflare-infrastructure)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
