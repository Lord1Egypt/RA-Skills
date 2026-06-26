# Attack Surface Checklist

Before hardening, identify what the agent can access and how it can be reached.

## 1. Channels

For each active channel, document:

- [ ] **Telegram** — enabled? DM policy? Group policy? AllowFrom list?
- [ ] **iMessage** — enabled? AllowFrom list? Group policy?
- [ ] **Discord** — enabled? Guild/channel restrictions? User restrictions?
- [ ] **Email (Gmail)** — can it read? Can it send? Which accounts?
- [ ] **Web/API** — any HTTP endpoints exposed? Auth required?
- [ ] **Webhooks** — any inbound hooks? Token-protected?

## 2. Tools and capabilities

- [ ] Can it execute shell commands? (`exec`)
- [ ] Can it read/write files? (`read`, `write`, `edit`)
- [ ] Can it spawn sub-agents? (`sessions_spawn`)
- [ ] Can it send messages to other channels? (`message`)
- [ ] Can it modify gateway config? (`gateway`)
- [ ] Can it manage cron jobs? (`cron`)
- [ ] Can it use a browser? (`browser`)
- [ ] Can it make outbound HTTP requests? (web search, web fetch, exec curl)
- [ ] Does it have access to MCP servers? (list each one below)

## 3. MCP server inventory

For each connected MCP, document:
- [ ] **Server name / source** — what service? Trusted provider or self-hosted?
- [ ] **Tools available** — list every tool the server exposes
- [ ] **Read vs write access** — can it only query, or can it create/update/delete?
- [ ] **Data sensitivity** — PII, credentials, financial data, PHI, proprietary info?
- [ ] **Exfiltration paths** — does this MCP + any outbound tool = data leak?
- [ ] **Tool descriptions reviewed** — checked for embedded injection?

See `references/mcp-hardening.md` for the full MCP audit process.

## 5. Data access

- [ ] What memory files can it read?
- [ ] Does it have access to credentials in `.env`?
- [ ] Can it access other users' sessions?
- [ ] Does it have access to connected services (Gmail, Drive, Slack, etc.)?
- [ ] Can it read the OpenClaw config including secrets?

## 6. Identity

- [ ] Does the agent have a verified owner identity?
- [ ] Are there allowlisted sender IDs?
- [ ] Can unauthorized users trigger the agent?
- [ ] Can other bots trigger the agent?

## Scoring

For each item checked, ask:
- **Is this access necessary for the agent's job?**
- **If compromised, what's the blast radius?**
- **Is there a deny list or restriction in place?**

Unnecessary access = unnecessary risk. Remove it.