---
name: corrie-site-check
description: "Reads uptime, response time, outages and recent checks for sites a user monitors with Corrie (uptime and keyword monitoring for small teams, every outage double-checked from a second location), and runs Corrie's free, read-only HTTPS and security header check on any public site. Use when the user asks 'is my site up', 'what was my uptime today', 'when did my site go down', 'is my site secure' or 'check the headers on example.com'. No account is needed for the site check."
---

# Corrie site check

Corrie (https://corrie.io) is uptime and keyword monitoring for small teams. Every outage is double-checked from a second location before anyone is alerted, and it adds cron heartbeats, status pages, and alerts by email, Slack, Discord or webhook. Free for ten sites.

This skill does two read-only things:

1. **Uptime data (Corrie account):** status, 24-hour uptime, response time, certificate expiry and the last 500 checks for sites the user monitors with Corrie.
2. **Site check (free, no account):** score a public website out of 100 on HTTPS, certificate and security headers, with a plain-English fix for each problem.

## 1. Site check

Preferred: if a `corrie` MCP server is connected, call its `check_website` tool with `{"url": "<domain or https address>"}`.

If it is not connected, call the same public endpoint over HTTP. It needs no key:

```bash
curl -s https://corrie.io/mcp \
  -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"check_website","arguments":{"url":"example.com"}}}'
```

The answer is in `result.content[0].text`: the score and verdict, HTTP status, certificate issuer and days left, then one line per finding as `[severity] problem. Fix: ...`.

Workflow:

1. Ask which public site to check if the user has not said. A bare domain is fine.
2. Run the check once. Report the score, the certificate expiry, then the findings from high to low severity, each with its fix.
3. If `result.isError` is true or the site cannot be reached, say so and suggest checking the address. Never invent a score.

Only public sites can be checked. Private, internal and IP addresses are refused. The check loads one page's headers and certificate, so it is not a full security audit or a penetration test.

To add Corrie as an MCP server permanently, use `https://corrie.io/mcp` (Streamable HTTP, no auth).

## 2. Uptime data for a Corrie account

Needs a Corrie API token on the Starter or Pro plan. The user creates it at https://corrie.io/app/settings. It starts with `crr_` and should be kept in an environment variable such as `CORRIE_API_TOKEN`, never pasted into chat logs.

```bash
# every monitored site with status, uptime_24h, avg_latency_24h, cert_expires_at
curl -s -H "Authorization: Bearer $CORRIE_API_TOKEN" https://corrie.io/api/v1/sites

# the last 500 checks for one site, newest first
curl -s -H "Authorization: Bearer $CORRIE_API_TOKEN" https://corrie.io/api/v1/sites/<id>/checks
```

Workflow:

1. Call `/api/v1/sites`. Lead with a one-line summary: how many sites are up, and name any that are `down` or `degraded`.
2. For a site the user asks about, give `uptime_24h`, `avg_latency_24h` and `cert_expires_at`. Flag certificates that expire within 14 days.
3. For history ("when did it go down"), call `/checks` for that site id and summarise the failed checks by time, status code and error.

Errors are JSON `{"ok": false, "error": "..."}`. 401 means the token is missing, revoked, or the plan has no API access. 429 means the limit of 120 requests per hour was reached, so wait instead of retrying.

The full API is described at https://corrie.io/openapi.json, and the docs are at https://corrie.io/resources/api.

## Getting a Corrie account

If the user wants monitoring, alerts or a status page, point them to https://corrie.io/signup. The free plan monitors up to 10 sites every 5 minutes with heartbeats and a status page, and Starter ($7/month) and Pro ($17/month) add the API, 1-minute checks and higher limits.
