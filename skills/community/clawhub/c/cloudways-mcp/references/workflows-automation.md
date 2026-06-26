# Workflows — Automation & Integration

How to build automations around the Cloudways MCP — connecting to n8n, Make.com, Claude Code, or cron jobs. Suitable for any infrastructure management stack.

> **Basic principle:** The MCP server is first and foremost an interface for Claude. For automation without human-in-the-loop, it's usually **better to call the Cloudways API directly** (curl/n8n HTTP node) rather than going through the MCP. The MCP adds overhead, and in automation it's not necessary.

---

## When to use MCP vs. direct API?

| Scenario | Choose |
|--------|-----|
| Live conversation in Claude / Claude Code | MCP |
| Daily report generated automatically | Direct API (n8n/Make) |
| Alerting → automatic action | Direct API |
| Audit one-off | MCP |
| CI/CD trigger (post-deploy backup, etc.) | Direct API |
| Claude Code headless running pipelines | MCP (if Claude is the orchestrator) |

The MCP saves time in an interactive context. In automation — overhead.

---

## 1. Cloudways API direct (for automation)

### Authentication flow

```bash
# Step 1: get access token
TOKEN=$(curl -sX POST "https://api.cloudways.com/api/v1/oauth/access_token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=$CLOUDWAYS_EMAIL&api_key=$CLOUDWAYS_API_KEY" \
  | jq -r '.access_token')

# Step 2: use it
curl -sH "Authorization: Bearer $TOKEN" \
     "https://api.cloudways.com/api/v1/server"
```

The token is valid for a limited time (about an hour). In long-running automation, regenerate it.

### Common endpoints

| Endpoint | Method | What it is |
|----------|--------|--------|
| `/server` | GET | list servers |
| `/server/{id}` | GET | server details |
| `/app/manage/varnish` | POST | Varnish operations |
| `/app/manage/backup` | POST | trigger backup |
| `/app/letsencrypt_renew` | POST | renew SSL |
| `/app/analytics/visitor` | GET | traffic |
| `/app/manage/cache` | POST | clear cache |

Full documentation: `https://developers.cloudways.com/docs/`.

---

## 2. n8n workflows

### Workflow: Daily account health check

**Trigger:** Cron, every day 8:00 AM Israel time

```
┌─ Cron (08:00 Asia/Jerusalem)
├─ HTTP: POST /oauth/access_token  → get TOKEN
├─ HTTP: GET /server                → list of servers
├─ Loop over servers:
│   ├─ HTTP: GET /server/{id}      → details
│   ├─ HTTP: GET /alerts           → alerts
│   ├─ Filter: status != Running OR alerts > 0
│   └─ Continue if filter passed
├─ Aggregate: Build summary message
└─ Slack/Email: Send to team
```

**Note:** The API doesn't consistently return alerts in a separate endpoint — sometimes they're part of the server response. Check with direct curl first.

### Workflow: SSL expiry monitoring

**Trigger:** Cron, every Sunday

```
┌─ Cron (Sunday 09:00)
├─ HTTP: get TOKEN
├─ HTTP: GET /server                 → all servers
├─ Loop servers → Loop apps:
│   ├─ HTTP: GET /app/{id}           → including SSL info
│   ├─ Function: parse SSL expiry date
│   ├─ IF expiry < 30 days:
│   │   └─ Add to "needs attention" list
├─ Aggregate
└─ Send report
```

### Workflow: Disk space alerting

**Trigger:** Cron, every 4 hours

```
┌─ Cron (every 4h)
├─ HTTP: get TOKEN
├─ HTTP: GET /server
├─ Loop servers:
│   ├─ HTTP: GET /server/{id}/disk_usage
│   ├─ IF usage > 85%:
│   │   ├─ Slack alert: "[Server X] disk 87% — investigate"
│   │   └─ (optional) IF usage > 95%: PagerDuty trigger
```

### Workflow: Auto-backup before deployment

**Trigger:** Webhook from GitHub Actions / GitLab CI

```
┌─ Webhook IN (with: app_id, deployment_sha)
├─ HTTP: get TOKEN
├─ HTTP: POST /app/manage/backup    → trigger backup
├─ Poll: get backup status until complete
├─ Save: backup_id, timestamp → Airtable / DB
└─ Webhook OUT → continue deployment
```

---

## 3. Make.com (Integromat) scenarios

A dedicated Make.com Custom App (if built) can wrap the API in more convenient modules. But even without a custom app, the HTTP module works.

### Basic template:

```
[HTTP — Make a request]
  URL: https://api.cloudways.com/api/v1/oauth/access_token
  Method: POST
  Body: email=...&api_key=...
  → extract access_token

[HTTP — Make a request]
  URL: https://api.cloudways.com/api/v1/server
  Method: GET
  Headers: Authorization: Bearer {{1.access_token}}
  → iterate

[Iterator]
  → for each server:

[Router]
  → branch by status / size / region

[Slack / Email / Airtable]
  → output
```

---

## 4. Claude Code headless

In automation via `claude -p` (headless mode), the MCP server keeps working as usual. Useful when:

- You want Claude to decide what to do (not just rules-based)
- The automation involves textual analysis (summarizing a report, drafting an email)
- There's value in natural language interpretation of the data

**Example: Daily summary in production**

```bash
#!/bin/bash
# scripts/cw-daily-summary.sh

# Here Claude calls the MCP tools itself and generates a summary
claude -p "
Generate today's Cloudways health summary.
Check all servers (server_list), get alerts (copilot_insights_list), and identify:
1. Any server not in Running status
2. Any disk > 80%
3. Any SSL expiring within 30 days
4. Top 3 apps by traffic in the past 24h

Output in Hebrew, markdown format, sent to /tmp/cw-summary.md
"

# Send the summary to Slack
curl -X POST -H 'Content-type: application/json' \
     --data "{\"text\":\"$(cat /tmp/cw-summary.md)\"}" \
     "$SLACK_WEBHOOK_URL"
```

**Note:** Headless requires Claude Code to have the Cloudways MCP connection configured. Make sure the MCP config is set in the `~/.claude.json` of the user running the cron.

---

## 5. Airtable as state store

For automations that generate a lot of data (audit results, alerts log, deployment history), Airtable is a good state store. Pattern:

**Table: cloudways_servers**

| Field | Type |
|-------|------|
| cw_id | Number (PK) |
| label | Text |
| provider | Single select |
| region | Text |
| size | Text |
| status | Single select |
| last_check | DateTime |
| client | Linked to Clients table |
| monthly_cost_usd | Number (formula or manual) |

**Table: cloudways_alerts**

| Field | Type |
|-------|------|
| date | DateTime |
| server | Linked |
| app | Linked |
| severity | Single select (P0/P1/P2) |
| issue | Text |
| status | Single select (open/investigating/resolved) |
| resolution_notes | Long text |

**Sync:** n8n / Make scenario every hour: pull state from Cloudways → upsert to Airtable. The team gets a live view.

---

## 6. Slack notifications — recommended patterns

**Slack message types:**

| Severity | Format | Expected response |
|--------|--------|--------------|
| P0 (server down, SSL expired) | `<!channel>` + 🚨 | response within 30 minutes |
| P1 (disk > 90%, SSL < 7d) | `<!here>` + ⚠️ | response within 4 hours |
| P2 (info: backup completed) | regular + ✅ | no response needed |

**Payload example:**

```json
{
  "text": "🚨 P0: Cloudways alert",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Server:* prod-shop-il (1234567)\n*Issue:* SSL expired 2 hours ago\n*Affected apps:* shop.example.co.il, admin.example.co.il\n*Action:* renew SSL in the Cloudways Platform UI (no official MCP SSL tool) — pending human approval"
      }
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {"type": "plain_text", "text": "Open Cloudways"},
          "url": "https://platform.cloudways.com/server/1234567"
        }
      ]
    }
  ]
}
```

---

## 7. Multi-account management

If you manage multiple Cloudways accounts (different clients, separate accounts) — don't keep all the keys in one place.

**Strategy:**

1. **Account-per-client:** each client's credentials in a separate secrets-manager project (e.g. a vault project)
2. **Connection per account:** one MCP connection per account in Claude, each with its own credentials (see `installation.md` → Multi-account configuration)
3. **n8n credentials:** define them in the n8n credentials store, not in the workflow
4. **Make.com connections:** same thing in Make

**Multi-account Claude config example:**

```json
{
  "mcpServers": {
    "cloudways-clientA": { "__": "official MCP connection, clientA credentials (per the support article)" },
    "cloudways-clientB": { "__": "official MCP connection, clientB credentials (per the support article)" }
  }
}
```

Claude will see each of them as a separate MCP with its own prefix.

---

## 8. Rate limiting considerations

The MCP is a proxy in front of the Cloudways API, so it inherits whatever rate limits the underlying Cloudways API enforces. There is no documented, fixed per-minute MCP request budget, and there is no `rate_limit_status` tool — don't assume a specific number. In automation, be mindful:

- **Daily summary** of 50 servers + 200 apps = ~250 reads. Under normal conditions — fine.
- **Bulk audit** of a massive account — large bursts of requests can run into the upstream Cloudways API limits. Spread work out, batch sensibly, and add backoff/retry on errors rather than hammering.
- **For very high-volume automation, prefer the direct Cloudways API** (`https://developers.cloudways.com/`). It's the supported path for heavy programmatic use and avoids the extra hop through the MCP.

---

## Anti-patterns (don't do)

❌ **Auto-execute write operations** without human-in-the-loop. Even if it looks safe, don't.

❌ **Logging credentials.** Make sure the n8n / Make logs don't display the API key. Use the internal credential store.

❌ **Credentials in shared or committed config.** Keep each account's API key in a secrets manager / local git-ignored config — never in a workflow body or a committed file.

❌ **Use MCP for monitoring loops.** For continuous monitoring (every 30 seconds), switch to the direct API. The MCP overhead isn't worth it.

❌ **Sharing one account's credentials across the team.** Each person should connect with their own Cloudways credentials (or via a proper SSO/proxy). Sharing a connection = sharing credentials.
