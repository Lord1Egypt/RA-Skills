---
name: cloudways-mcp
version: 1.5.3
license: MIT
description: |
  Operational guide for managing Cloudways servers and applications, across one or several Cloudways accounts, via the official Cloudways MCP server (Cloudways' hosted MCP / Remote MCP, per their support docs).
  Use whenever the user mentions Cloudways, a Cloudways server or app, server monitoring, app monitoring, bandwidth, disk usage, PHP/MySQL/traffic analytics, Varnish cache, app cloning, backups/restore on Cloudways, Git deployments on Cloudways, SSL/Let's Encrypt on Cloudways, malware scans / Security Suite, staging sync, team members, AgencyOS client billing, or running an audit/onboarding on a Cloudways-hosted client site.
  Any write operation (start/stop/restart server, backup, restore, update CNAME, purge cache, change service state, git pull, SSL install/revoke, IP whitelist update, staging sync, team/billing changes, delete server/app) requires explicit confirmation of target server/app and intended action before execution.
---

# Cloudways MCP — Operational Skill

Managing Cloudways infrastructure through the Cloudways MCP server.

> **Connection:** This skill targets the **official Cloudways (Remote) MCP** — an MCP hosted by Cloudways at `https://mcp.cloudways.com/mcp/` that you connect to directly. The source of truth for connecting is the **official article**: `support.cloudways.com/en/articles/14654372`. See `references/installation.md`.
>
> **Tool names match the official articles.** The tool catalog and workflows in this skill use the official Cloudways MCP tool names (verified against the setup article and the dedicated [tools article](https://support.cloudways.com/en/articles/15798823-cloudways-mcp-server-tools)). Always treat the live `mcp__cloudways*__*` tools as the source of truth if Cloudways changes them (see "Versioning and source of truth" below).

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

6. **Credentials.** Each account authenticates with its own **Access Token** (case-sensitive `X-Access-Token` header; roles + legacy-key migration in the Authentication section below). Don't print tokens in responses. Don't mix credentials between accounts. If the user asks to see them, refer them to platform.cloudways.com → API section.

7. **Don't sweep the credential-returning tools.** `server_get`, `app_get` and `app_credentials` return master, database and SSH credentials inside their ordinary payloads. Running one of them over **every** server or **every** app pulls the account's secrets into the conversation, where they stay for the rest of it — and telling yourself to keep them out of the *report* comes too late to help. Use `server_list` / `app_list` for inventory; call the other three for a specific field nothing else returns, or for a task the user actually asked for.
   **But do not read "inventory" as "credential-free."** The live server describes `app_list` as returning “ID, label, application type, version, domain, **and credentials**”, and both list tools are built from the same `GET /server` payload that makes `server_get` a credential tool. What makes them the right choice is that they answer the inventory question in **one call per account or per server** instead of one per app — not that their responses are known to be clean. Take the IDs and the fields you came for; never paste a raw list response into a report, a ticket or an automation. And when a job requires that no credential enter the transcript **at all**, build the roster outside the conversation — the Cloudways Platform UI, or a direct `GET /server` piped through a field filter on your side — and bring back only ids and labels.

8. **Read-only by default.** If the user just asks "show me / check / monitor" — always choose the appropriate read-only tool. Don't suggest a destructive operation unless the user explicitly asked for it.

9. **`execute_tool` / toolset-proxy calls inherit their target tool's R/W/W! risk.** Most tools live in on-demand toolsets and are invoked through the `execute_tool` proxy (or surfaced via `get_toolset_tools`). Calling a write/destructive tool through the proxy is exactly as consequential as calling it directly — apply the **same** confirmation (and double-confirmation for W!) as you would for the named tool.

---

## Write operations require confirmation — the catalog is authoritative

**The authoritative list is `references/tools-catalog.md`: every tool flagged `W` or `W!` there requires explicit confirmation before execution, and every `W!` requires the double-confirmation pattern.** The grouping below is **illustrative, not exhaustive** — the live MCP (v1.2) exposes 244 tools — 241 across 22 toolsets plus 3 meta-tools — and 179 of them are **not** in your default tool list. If a tool is not named here but is flagged `W`/`W!` in the catalog (or its live schema describes a destructive/irreversible action), it needs the **same** confirmation. Never treat "it's not in this list" as "it's safe to run without confirmation."

**Server level (affects all applications on the server):**
- `server_start`, `server_stop`, `server_restart`
- `server_delete` ⚠️⚠️ (W! — immediate destruction)
- `server_scale` ⚠️ (W! — resize CPU/RAM with brief downtime for every app on the server)
- `server_backup`, `server_backup_settings_update`, `server_snapshot_frequency_update`
- `server_local_backup_delete` ⚠️ (W! — permanently deletes local backup snapshots)
- `server_package_update` (W! for the uninstall variant — removes a package + its data)
- `server_master_username_update`, `server_master_password_update` ⚠️ (W! — old SSH/SFTP creds stop working immediately)
- `service_start`, `service_stop`, `service_restart` (Apache/Nginx/Memcached/MySQL/Varnish)
- `varnish_manage`

**App level:**
- `app_create`, `app_clone`, `app_clone_to_server`, `staging_app_clone`, `staging_app_clone_to_server` (create new copies — consume resources)
- `app_backup`, `app_restore` ⚠️⚠️ (W! — full overwrite of current state)
- `app_restore_rollback` ⚠️ (W! — overwrites current state with the pre-restore copy; only within the rollback window)
- `app_local_backup_delete` ⚠️ (W! — permanently deletes the local pre-restore snapshot)
- `app_delete` ⚠️⚠️ (W! — immediate destruction)
- `app_db_password_update`, `app_admin_password_update`, `app_credentials_update`, `app_credentials_delete` ⚠️ (W! — old credentials stop working immediately)
- `app_enforce_https_update`, `app_stack_update`, `app_reset_permissions`, `app_wp_multisite_update`
- `app_cname_update`, `app_cname_delete` ⚠️ (W! — can break production)
- `app_purge_cache`, `varnish_app_manage`

**DNS / Projects / SSH keys (live via their toolsets):**
- `dns_made_easy_delete_domains`, `dns_made_easy_delete_records` ⚠️ (W! — DNS records/domains gone; can break mail + site resolution)
- `project_delete` ⚠️ (W! — ungroups the project)
- `ssh_key_delete` ⚠️ (W! — revokes SSH/SFTP access immediately)

**Add-ons:**
- `addon_activate`, `addon_activate_on_server`, `addon_deactivate`, `addon_deactivate_on_server` (W — can change the account subscription / incur cost)

**Security — SSL & IP access (new in MCP v1.2):**
- `security_lets_encrypt_install`, `security_lets_encrypt_renew`, `security_lets_encrypt_auto_renewal`
- `security_lets_encrypt_revoke`, `security_remove_own_ssl` ⚠️ (W! — HTTPS breaks until a new cert is installed)
- `security_update_whitelisted_ips` ⚠️ (W! — **replaces** the SSH/SFTP or MySQL whitelist; a wrong list locks people out — always read the current list first)
- `security_whitelist_ip_siab`, `security_whitelist_ip_adminer`

**Security Suite / staging / team / transfer (new in MCP v1.2):**
- `security_suite_app_files_restore` ⚠️ (W! — restoring quarantined files can put malware back on the live site)
- `security_suite_server_countries_blacklist_update` ⚠️ (W! — blocks all traffic from entire countries)
- `staging_sync_tables`, `staging_sync_code` ⚠️ (W! — overwrite data/code on the target; confirm **direction** — a push to live overwrites production)
- `team_member_update`, `team_member_delete` ⚠️ (W! — changes/revokes a person's access)
- `server_transfer_request` ⚠️ (W! — hands server **ownership** to another Cloudways account)
- `agency_os_*` create/update (W — client-facing financial records: clients, services, plan prices, tax rates, invoices)
- `agency_os_client_delete` ⚠️ (W! — deletes a client-facing financial record, archiving their services + invoice history)
- `copilot_subscribe`, `copilot_plan_change`, `addon_upgrade` (W — change the account's subscription cost)

**Git deployment:**

- `git_clone`, `git_pull` (can break production if there's a conflict)
- `git_generate_key` ⚠️ (W! — overwrites the app's existing deploy key; the old key stops working)

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

The official MCP is hosted at `https://mcp.cloudways.com/mcp/` and authenticates via two **case-sensitive** HTTP headers:

- `X-Access-Token` — a Cloudways **Access Token** generated in the platform
- `X-Mcp-Host` — the client identifier (`claude-code` / `claude-desktop`; full list of official values in `references/installation.md`)

Tokens are **role-based (RBAC)**: **READ** (look-ups only), **LIMITED** (selected endpoint groups), **FULL ACCESS** (everything, including destructive actions). Start new integrations with READ and escalate only when a connection must write. This platform-level control **complements** (does not replace) this skill's write-confirmation discipline — even FULL ACCESS has no per-tool gating at the MCP layer.

> **Legacy:** the old `X-CW-Email` + `X-CW-Api-Key` API-key headers are deprecated — the API key stops working on **October 15, 2026** — and until migrated such connections retain unrestricted full-account access. Migration: `references/installation.md`.

Treat tokens like passwords and **never print them in responses**. If the user asks to see one, refer them to platform.cloudways.com.

For the full connection, role guidance, and multi-account setup, see `references/installation.md`.

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
- **Credentials don't mix.** Each connection has its own Access Token. Don't assume the same credentials work on another account.

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
1. server_list                  → the fleet (server_get would add master credentials)
2. monitoring_server_graph      → metrics (CPU/mem/etc.)
3. app_list                     → per server, the application roster. server_list returns an
                                  app COUNT, not the IDs step 4 needs. One call per server,
                                  and rule 7 on what that one payload may carry
4. monitoring_app_summary       → for each application from step 3
5. copilot_insights_list        → open insights/alerts
6. monitoring_server_summary    → disk/bandwidth; if disk > 80% — red flag
```

### Checking an app's details
```
1. app_list                  → find the app: id, label, type, version, domain
2. app_settings_get          → its setting flags (XML-RPC, GEO-IP, password protection, …)
3. monitoring_app_summary    → what it is doing right now
```

(`app_get` is not in this list on purpose: it returns the application's **database
credentials** beside fields the three calls above already give you. Step 1 is the roster you
usually already hold from this conversation. Every app-scoped call takes a `server_id` beside
the app id — `app_settings_get` and `monitoring_app_summary` included — so an app id on its own
runs **nothing**, read or write; if you do not know the server, ask for it or for the app's
name/URL. What differs between a read and a write is confirmation: a read on a known
server/app pair can simply run, while a **write** needs name + URL from the roster first — a
mistyped id that belongs to another app is still a valid id. When you hold no roster: for a
**name** you are looking up, `app_list` on the server is the one API route (one call; rule 7
says what its payload may carry — take the one row, paste none of it); for an **id** you already
know, `app_list` is the wrong tool, because it covers every app on the server, and one
`app_get` for that app — or the app's page in the UI — exposes strictly less. Reach for
`app_get` otherwise only for a field none of these return, and accept what comes with
it.)

(SSL / Let's Encrypt **is** an MCP tool as of v1.2 — `security_lets_encrypt_install` / `_renew` / `_auto_renewal` / `_revoke`, via the security toolset. Install/renew are W; revoke is W!.)

For more detailed patterns, load the relevant workflows.

---

## Versioning and source of truth

- **Tool names match the official articles.** The tool names and categories in this catalog are **verified** against the official Cloudways support articles (setup + tools reference, MCP v1.2). They are the official MCP tool names. The v1.2 additions have not yet been re-enumerated against the live server — see the note in `references/tools-catalog.md`.
- **The live MCP remains the source of truth if Cloudways changes them.** If a tool name or capability differs from what's documented here, the live list of tools connected in Claude (`mcp__cloudways*__*`) wins — check it and update the catalog accordingly.
- **Every write tool still goes through the confirmation pattern.** W = single confirmation, W! = double-confirmation (destructive — e.g. `server_delete`, `app_delete`, `app_restore`, `app_cname_delete`), per `references/tools-catalog.md`. This discipline is **more** important now that the official destructive tools are confirmed to exist.
