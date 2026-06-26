---
name: cloudways-mcp
version: 1.2.1
license: MIT
description: |
  Operational guide for managing Cloudways servers and applications, across one or several Cloudways accounts, via the official Cloudways MCP server (Cloudways' hosted MCP / Remote MCP, per their support docs).
  Use whenever the user mentions Cloudways, a Cloudways server or app, server monitoring, app monitoring, bandwidth, disk usage, PHP/MySQL/traffic analytics, Varnish cache, app cloning, backups/restore on Cloudways, Git deployments on Cloudways, or running an audit/onboarding on a Cloudways-hosted client site. (SSL/Let's Encrypt and SSH/MySQL IP whitelisting are not MCP tools — do those in the Cloudways UI or direct API.)
  Any write operation (start/stop/restart server, backup, restore, update CNAME, purge cache, change service state, git pull, delete server/app) requires explicit confirmation of target server/app and intended action before execution.
---

# Cloudways MCP — Operational Skill

Managing Cloudways infrastructure through the Cloudways MCP server.

> **Connection:** This skill targets the **official Cloudways (Remote) MCP** — an MCP hosted by Cloudways at `https://mcp.cloudways.com/mcp/` that you connect to directly. The source of truth for connecting is the **official article**: `support.cloudways.com/en/articles/14654372`. See `references/installation.md`.
>
> **Tool names match the official article.** The tool catalog and workflows in this skill use the official Cloudways MCP tool names (verified against the support article). Always treat the live `mcp__cloudways*__*` tools as the source of truth if Cloudways changes them (see "Versioning and source of truth" below).

> **Context:** The skill is built for day-to-day work managing clients/environments on Cloudways — monitoring, routine maintenance, onboarding/audit for new clients, and automations. All monetary values reported by the API are in $ (USD), not ₪.

---

## Quick Route

| Intent | Load |
|--------|------|
| Initial installation/configuration of the MCP server | `references/installation.md` |
| Don't know which tool exists / searching for a tool by name | `references/tools-catalog.md` |
| Monitoring, status check, bandwidth, analytics | `references/workflows-monitoring.md` |
| Cache clear, SSL, backup, restart, IP whitelist | `references/workflows-maintenance.md` |
| New audit / onboarding a new client | `references/workflows-onboarding.md` |
| Building an automated workflow for n8n/Make/Claude Code | `references/workflows-automation.md` |
| Multiple Cloudways accounts / multi-account configuration | `references/installation.md` (Multi-account section) |

**Load only what's needed.** Maximum 2-3 references per task. If the user just asks "show me my servers", don't load the entire catalog — call `server_list` directly.

---

## Safety rules (read before every operation)

1. **Selecting the correct account — before anything else (multi-account).** There are **multiple Cloudways accounts**, each as a separate MCP connection with its own prefix (e.g. `mcp__cloudways-clientA__*`). Before every call — verify which account it belongs to. If more than one account is connected and it's not clear from context which one is meant — **stop and ask**, don't guess. server/app IDs are **not interchangeable between accounts** — ID 1234567 in account A is an entirely different resource (or nonexistent) in account B. Don't take an ID from one account's response and run it against another account. See the "Multi-account" section below.

2. **Write operations require explicit confirmation.** Before every call to a tool that belongs to the Write category (see list below), present to the user: **the account**, the tool name, the target server/application (ID + name), the parameters, the expected impact. Wait for a confirmation response before executing. Don't assume that confirming one operation grants confirmation for further operations — nor that confirmation on one account applies to another.

3. **Backup before a significant change.** Before `app_restore`, `app_delete`, `varnish_manage`, `varnish_app_manage`, or any configuration change — check with the user whether a recent backup exists. If not, offer to run `app_backup` / `server_backup` first.

4. **Multiple services = multiplied risk.** Cloudways usually hosts **several applications on the same server**. `server_stop`, `server_restart`, or `server_delete` affects **all** the applications. Always make sure the user is aware of the list of applications on the server before a server-level operation.

5. **`server_delete`, `app_delete`, and `app_cname_delete` = immediate destruction in production.** Requires double confirmation (W!): of both the operation and the specific domain/application/server.

6. **Credentials.** Each account has its own API key + email, passed through case-sensitive HTTP headers (`X-CW-Email`, `X-CW-Api-Key`). Don't print them in responses. Don't mix credentials between accounts. If the user asks to see them, refer them to platform.cloudways.com → API Integration.

7. **Read-only by default.** If the user just asks "show me / check / monitor" — always choose the appropriate read-only tool. Don't suggest a destructive operation unless the user explicitly asked for it.

---

## Write operations — full list by category

For each of the following operations, **explicit confirmation is mandatory before execution**:

**Server level (affects all applications on the server):**
- `server_start`, `server_stop`, `server_restart`
- `server_delete` ⚠️⚠️ (W! — immediate destruction)
- `server_backup`
- `service_start`, `service_stop`, `service_restart` (Apache/Nginx/Memcached/MySQL/Varnish)
- `varnish_manage`

**App level:**
- `app_create`, `app_clone`, `app_clone_to_server` (create new copies — consume resources)
- `app_backup`, `app_restore`
- `app_delete` ⚠️⚠️ (W! — immediate destruction)
- `app_enforce_https_update`
- `app_cname_update`, `app_cname_delete` ⚠️ (can break production)
- `app_purge_cache`, `varnish_app_manage`

> **SSL / Let's Encrypt and IP whitelisting (SSH/MySQL) are NOT MCP tools.** The official Cloudways MCP exposes no SSL, Let's Encrypt, or IP-whitelist tools. Do these in the Cloudways Platform UI or via the [direct Cloudways API](https://developers.cloudways.com/).

**Git deployment:**

- `git_clone`, `git_pull` (can break production if there's a conflict)
- `git_generate_key`

---

## Confirmation pattern for a destructive operation

Before execution, present a block like this:

```
🔒 Confirm operation execution?
   Account: clientA (mcp__cloudways-clientA)
   Tool: server_stop
   Server: production-shop-il (ID: 1234567)
   Applications affected: woocommerce-prod, staging-clone, admin-tools
   Impact: all 3 applications will be offline until a manual restart
   Proceed? (yes / no / pause and check backup first)
```

Wait for an explicit response. A literal "yes" only = confirmation. Implied consent is not enough. The **account line is mandatory** when more than one account is connected — it prevents executing an operation on the wrong account.

---

## Authentication — quick overview

The official MCP is hosted at `https://mcp.cloudways.com/mcp/` and authenticates via three **case-sensitive** HTTP headers:

- `X-CW-Email` — the Cloudways account email
- `X-CW-Api-Key` — the API key from platform.cloudways.com → **API Integration**
- `X-Mcp-Host` — the client identifier, value `claude-code` or `claude-desktop`

The API key has **full account access** — it grants every action the account can perform in the UI. There is **no granular / per-tool permission at the MCP layer**: any connected client can call any tool. Treat the key like a password and **never print it in responses**. If the user asks to see it, refer them to platform.cloudways.com → API Integration.

For the full connection and multi-account setup, see `references/installation.md`.

---

## Multi-account — working with multiple Cloudways accounts

There are usually **multiple Cloudways accounts** (different clients / different environments). Each account is connected as a **separate** MCP connection with its own credentials, and therefore appears in Claude with **its own prefix**:

```
mcp__cloudways-clientA__server_list
mcp__cloudways-clientB__server_list
mcp__cloudways-internal__server_list
```

> The configuration (how multiple accounts are connected — one connection per account, each with its own credentials) is documented in `references/installation.md` section **Multi-account configuration**. The runtime rules are here.

### The golden rule: identify the account before every operation

1. **A single account connected** → use it, no need to ask.
2. **Multiple accounts connected** → determine which account the request belongs to **before** you call a tool:
   - If the user explicitly specified a client/account ("check clientB's prod") → use the matching connection.
   - If the server/domain name unambiguously identifies a single account → you may infer, but explicitly state which account you're operating on.
   - If **it's unclear** → stop and ask: "Which account? (clientA / clientB / internal)". Don't guess, and don't run on all of them "just to be safe".

### Complete isolation between accounts

- **IDs don't cross accounts.** A server_id / app_id you received from `mcp__cloudways-clientA` is valid **only** against clientA. Never take an ID from one account's response and pass it to a tool of another connection.
- **Per-account confirmation.** A write confirmation on one account does not apply to another. Every write operation on a new account = a new confirmation block (including the account line).
- **Credentials don't mix.** Each connection has its own email + API key. Don't assume the same credentials work on another account.

### Cross-account search (read only)

When the user asks for something broad — "which account does the domain shop.example.co.il live on?", "give me a disk overview for all accounts" — it's permitted and legitimate to **read (read-only)** from all the connections, but:
- Run the same sequence of reads on each connection **separately**, and tag each result with the account name.
- Summarize in a table with a clear "Account" column.
- **Never** perform a broad write operation across multiple accounts without individual confirmation for each one.

```
Example tagging in the response:
| Account  | Server           | disk |
|----------|------------------|------|
| clientA  | prod-shop-il     | 87%  |
| clientB  | prod-blog        | 41%  |
| internal | ops-tools        | 63%  |
```

---

## Common usage patterns (examples)

### Quick snapshot of an account
```
1. server_list               → list of all servers
2. copilot_insights_list     → active insights/alerts
```

(No account/whoami tool exists — infer the account from the connection prefix + `server_list`.)

### Health check before a weekend (production client)
```
1. server_get                   → CPU/RAM/disk
2. monitoring_server_graph      → metrics (CPU/mem/etc.)
3. monitoring_app_summary       → for each application
4. copilot_insights_list        → open insights/alerts
5. monitoring_server_summary    → disk/bandwidth; if disk > 80% — red flag
```

### Checking an app's details
```
1. app_list                  → find the app
2. app_get                   → details, FQDN, config
```

(SSL / Let's Encrypt is **not an MCP tool** — manage and renew certificates in the Cloudways UI or via the direct Cloudways API.)

For more detailed patterns, load the relevant workflows.

---

## Versioning and source of truth

- **Tool names match the official article.** The tool names and categories in this catalog are **verified** against the official Cloudways support article. They are the official MCP tool names.
- **The live MCP remains the source of truth if Cloudways changes them.** If a tool name or capability differs from what's documented here, the live list of tools connected in Claude (`mcp__cloudways*__*`) wins — check it and update the catalog accordingly.
- **Every write tool still goes through the confirmation pattern.** W = single confirmation, W! = double-confirmation (destructive — e.g. `server_delete`, `app_delete`, `app_restore`, `app_cname_delete`), per `references/tools-catalog.md`. This discipline is **more** important now that the official destructive tools are confirmed to exist.
