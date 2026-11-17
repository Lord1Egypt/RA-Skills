# Workflows — Onboarding & Audit (agency client takeover)

Core scenario: a new client arrives with a site on Cloudways, and you need to build a complete picture — no crashes, no surprises at 3 AM.

> **Guiding principle:** On the first audit, **don't touch anything.** Just read. Full documentation of the current state first. Changes come after you understand the picture and have a structured plan.

---

## Stage 0 — Pre-flight (before calling MCP)

Confirm with the client:
- [ ] API access approved on their side
- [ ] A **new Access Token** generated for this engagement (READ role for the audit phase; don't reuse tokens their old team held — old tokens should be revoked). One exception: `server_disk_usage_fetch` (Stage 2) is classified W and may be blocked on a READ token — either rely on the cached `monitoring_server_summary`, or scope a LIMITED token that includes it.
- [ ] If there are old team members who don't need access — plan the removal now; as of MCP v1.2 the roster is auditable via `team_member_list` (R) and removal is `team_member_delete` (W! — double-confirm, do it only after the audit)

---

## Stage 1 — Account mapping

```
1. server_list                 → all servers: count, providers, regions, sizes (this is the entry point — infer the account from the connection prefix; there is no whoami/customer_info tool)
2. project_list                → how they're organized
3. copilot_insights_list       → insights, alerts, and recommendations currently open
```

> **No MCP tool for:** account/plan/billing status (`customer_info`) or SSH-key listing. Plan/billing is checked in the Cloudways Platform UI; SSH keys are managed via `ssh_key_create` / `ssh_key_update` / `ssh_key_delete` and there is no list tool; the roster does come back inside `server_get`, next to that server's master credentials, so for an audit confirm SSH access in the UI or via the direct Cloudways API instead (<https://developers.cloudways.com/>). The **team-member roster IS available** as of MCP v1.2: `team_member_list` (R) returns sub-users with roles and server/app access.

**Deliverables you record:**

| Field | Value |
|------|-----|
| Cloudways plan | (Starter/Growth/Enterprise? — UI only) |
| Number of servers | |
| Providers in use | (DO/AWS/GCP/Vultr) |
| Regions | |
| Total monthly $ Cloudways (estimate) | |
| Team members + permissions | (`team_member_list`) |
| SSH keys (don't publish — only a count) | (UI / direct API) |
| Open insights/alerts | (copilot_insights_list) |

---

## Stage 2 — Server mapping

Stage 1's `server_list` already carries each server's label, size, provider, region, IP and
app count, in one call for the whole account — see safety rule 7 on what a list payload may
still contain. For each server in that list:

```
1. server_settings_get         → PHP timeout, memory, upload limit, custom PHP
2. service_status              → what's running (Apache/Nginx/MySQL/Memcached/Varnish/Redis)
3. server_disk_usage_fetch     → optional: trigger a fresh disk-usage calculation (W — benign refresh, but may be blocked on a READ token; skip and use the cached data if so), then:
4. monitoring_server_summary   → current disk + bandwidth usage (read; cached values if step 3 was skipped)
5. monitoring_server_graph     → CPU/RAM trends last 24h
```

**Red flags to watch for:**
- [ ] Disk > 80% → can't add content without risk
- [ ] Sustained CPU spike → performance problem
- [ ] PHP timeout < 60s → may break long operations
- [ ] memory_limit < 256M → WordPress will get stuck
- [ ] Memcached/Redis off → no object caching
- [ ] Varnish off → no page caching
- [ ] Server hosting 5+ apps from different sources → high blast radius

---

## Stage 3 — Application mapping

`app_list` gives the roster per server in one call — the application IDs every step below needs,
which `server_list`'s app *count* cannot supply. Read rule 7 before pasting any of it anywhere.
For each application in it:

```
1. app_settings_get            → app-level overrides + security flags (XML-RPC, password protection, etc.)
2. monitoring_app_summary      → bandwidth, requests (to get a sense of scale)
3. analytics_app_traffic       → visitors at least last 7 days (drill in with analytics_app_traffic_details)
4. analytics_app_php           → slow scripts? memory issues?
5. analytics_app_mysql         → slow queries?
6. app_varnish_settings_get    → cache configured?
7. app_vulnerabilities_list    → (WordPress) known plugin/theme/core vulnerabilities
```

> **Do not CALL the credential-returning tools during discovery.** Not "call them and leave
> the secrets out of the report" — by then they are already in the transcript, and a
> transcript is kept, scrolled back through, and sometimes pasted somewhere. The only way to
> keep a credential out of a conversation is not to fetch it.
>
> So this pass uses `server_list` and `app_list` — **one call per account and one per server**,
> instead of a credential payload per app — and gets its detail from `server_settings_get`,
> `service_status`, `app_settings_get`, the monitoring and analytics tools and
> `app_vulnerabilities_list`, none of which is documented to return credentials.
>
> That is a reduction, not a guarantee, and it is worth being exact about which: the live server
> describes `app_list` itself as returning “… domain, **and credentials**” (safety rule 7). This
> MCP exposes no roster endpoint documented to exclude them, so an app-level audit costs one such
> payload per server. **If the engagement requires that no credential enter the transcript at
> all, build the roster outside the conversation** — the Cloudways Platform UI, or a direct
> `GET /server` piped through a field filter on your side — and hand the agent only the ids and
> labels. What is not acceptable is the shape this release removed: one credential payload per
> application, fetched by the agent, for an inventory that needed none of it.
>
> Three tools are deliberately NOT here:
>
> - **`app_credentials`** — SSH/SFTP access. An inventory never needs it. Call it when a task
>   the user actually asked for needs it, such as an SFTP deploy.
> - **`server_get`** — richer per-server configuration, and **master credentials** in the same
>   payload. Reach for it only when you need something the list and settings tools do not
>   carry, knowing the secrets come with it. The SSH-key roster is the usual example, and for
>   an AUDIT it is the wrong trade — see the note below.
> - **`app_get`** — URL, FQDN and app folder, and **database credentials** in the same
>   payload. Same rule: call it for a specific missing field, not for every app in a sweep.
>
> Onboarding an unfamiliar fleet is exactly when a broad sweep feels harmless and is not. One
> pass over a 20-server account, done the old way, pulled every server's master password and
> every application's database password into one conversation — and a report is not the only
> thing that outlives an engagement.

> **No dedicated SSH-key list tool either, and the same answer.** Keys are managed with
> `ssh_key_create` / `_update` / `_delete`; the roster comes back inside `server_get`, next to
> that server's **master credentials**. For an audit, read it in the Cloudways Platform UI or
> via the direct API and record a count rather than the keys — the deliverables table already
> asks for a count, not a list.

> **No dedicated SSL read tool — and the one payload that carries the detail is not worth a
> sweep.** There is no `ssl_get`; certificate provider and expiry come back inside `app_get`,
> which also returns that application's **database credentials**. For an audit across a whole
> fleet that is a bad trade, so read provider + expiry from the Cloudways Platform UI or the
> direct API here. **The same answer applies to the weekly review**: `workflows-monitoring.md`
> §5 no longer walks the fleet with `app_get` at all — it collects the dates outside the
> conversation and brings back only names and dates. In the agent, `app_get` is for one
> certificate somebody named.

> **Domains: the primary comes from the roster, the aliases do not.** `app_list` documents a
> `domain` field, so the primary domain arrives with the roster you already fetched. There is no
> read tool for the secondary ones: `app_cname_update`, `app_cname_delete` and
> `app_aliases_update` are all **writes**, and nothing in the catalog lists the aliases back. So
> read additional domains/CNAMEs from the Cloudways Platform UI or the direct API, exactly as
> with SSL — and never call a W tool to inspect a value.

**Deliverables table for each app:**

| Field | Value | red flag? |
|------|-----|-----------|
| App name | | |
| Primary domain | app_list (`domain`) | |
| Additional domains/CNAMEs | UI / API | |
| SSL provider + expiry | UI / API | check auto-renew? |
| App type (WP/Magento/PHP/Laravel) | | |
| PHP version | | < 8.1 = upgrade needed |
| WP version (if relevant) | | < 6.0 = security risk |
| Known vulnerabilities (if WP) | app_vulnerabilities_list | any open CVEs? |
| Active plugins (if WP) | manual | abandoned plugins? |
| DB size (rough) | | |
| Daily traffic (avg) | | |
| Daily bandwidth | | |
| Avg response time | | > 1.5s = problem |
| Backups schedule | | none = critical risk |
| Varnish enabled | | false = perf gap |
| Object cache | | none = perf gap |
| HTTPS enforced | | false = SEO+security gap |

---

## Stage 4 — Security audit

```
1. app_settings_get                    → per-app security flags (XML-RPC enabled? password protection?)
2. app_vulnerabilities_list            → (WordPress) open plugin/theme/core vulnerabilities
3. copilot_insights_list               → security-related insights/recommendations Cloudways has surfaced
4. security_get_whitelisted_ips        → (v1.2) SSH/SFTP IP whitelist per server
5. security_get_whitelisted_ips_mysql  → (v1.2) MySQL IP whitelist per server
6. team_member_list                    → (v1.2) who still has access, with which role
7. security_suite_app_status_get       → (v1.2, if Security Suite is active) protection status per app
8. security_suite_server_incidents_list→ (v1.2) open security incidents on each server
```

> **Still no SSH-key LIST tool.** Keys are managed via `ssh_key_create` / `ssh_key_update` / `ssh_key_delete`, and the roster rides inside `server_get` beside that server's master credentials — so for an audit read it in the Cloudways Platform UI (Server → Security) or via the direct Cloudways API (<https://developers.cloudways.com/>), and record a count rather than the keys.

**Red flags (now readable via MCP; SSH-key roster still UI/API):**
- [ ] SSH whitelist empty = open to the world (critical)
- [ ] MySQL whitelist empty = open to the world (security disaster)
- [ ] Old SSH keys whose owners are unclear (UI/API)
- [ ] The old team member still has access (`team_member_list`)
- [ ] Access not only for client employees but also for employees who have left
- [ ] XML-RPC left enabled on WordPress (`app_settings_get`) = brute-force/DDoS vector
- [ ] Open vulnerabilities reported by `app_vulnerabilities_list`
- [ ] Open Security Suite incidents / infected domains (`security_suite_server_incidents_list`, `security_suite_server_infected_domains_list`)

---

## Stage 5 — Backups audit

The official Cloudways MCP has no "list all backups" tool. `app_backup_status_get` reports only whether a backup is currently **in progress** for an app, and backup scheduling is changed via `server_backup_settings_update`. To audit the existing schedule and retention you still need the UI (or a direct API call).

**Questions to check manually:**
- Are automatic backups enabled? (Cloudways → Server → Backups)
- Frequency? (daily / every two days / weekly)
- Retention? (how many days back?)
- Is there an off-platform backup? (Cloudways backups are available only from within Cloudways — if the account is closed, they're lost)

**Standard recommendation:**
- Daily Cloudways backups, 7-day retention
- Weekly off-platform backup (UpdraftPlus to S3 / Wasabi / Cloudways → Drive)

---

## Stage 6 — Reporting to the client

The onboarding document must include (Hebrew):

### 1. Executive summary
- How many servers, how many apps, rough monthly spend
- The 3-5 most severe red flags you found
- General recommendation (priority order)

### 2. Detailed current state
- Tables for each server + each app
- Links / IDs in Cloudways

### 3. Recommended task list
By priority (P0/P1/P2):

**P0 — must be done within the coming week:**
- (security criticalities: expired SSL, open whitelist, etc.)

**P1 — must be done within the month:**
- (PHP/WP upgrades, backup strategy, performance)

**P2 — long-term improvements:**
- (CDN integration, Varnish tuning, monitoring setup)

### 4. Quote
Estimated hours per P (₪300/h). Everything documented.

### 5. SLA / operational routine
- Weekly monitoring (which queries will be run)
- Response to an alert (target time)
- SSL renewals — who is responsible

---

## Quick report template

```markdown
# Cloudways Audit — [Client Name]
Date: [YYYY-MM-DD]
Auditor: [your name]

## Summary
- Servers: X | Apps: Y | Monthly spend (gross): $Z
- Critical findings: [N items]
- Recommendation summary: [one paragraph]

## Red flags
| Severity | Issue | Impact | Effort to fix |
|----------|-------|--------|---------------|
| P0 | ... | ... | ... |

## Inventory
(tables from stages 2-3)

## Recommended actions
### Phase 1 (week 1) — P0 items
### Phase 2 (month 1) — P1 items
### Phase 3 (ongoing) — P2 items

## Quote
| Phase | Hours | ₪ |
|-------|-------|---|
| 1 | ... | ... |
| 2 | ... | ... |
| **Total** | | |
```

---

## Quick reference — Audit checklist (printable)

- [ ] **Account:** server_list / project_list / copilot_insights_list / team_member_list  (plan/billing = UI only)
- [ ] **Per server:** server_settings_get / service_status / monitoring_server_summary / monitoring_server_graph (optionally server_disk_usage_fetch first for fresh disk data — W, needs a token role that allows it)
- [ ] **Per app:** app_list for the roster, then app_settings_get / monitoring_app_summary / analytics_app_traffic / analytics_app_php / analytics_app_mysql / app_varnish_settings_get / app_vulnerabilities_list (WP)
- [ ] **NOT in a sweep:** `server_get`, `app_get`, `app_credentials` — each returns master, database or SSH credentials in its payload, so a per-server or per-app loop pulls the whole account's secrets into the conversation. Call one for a specific missing field, or for a task the user asked for. See Stage 2.
- [ ] **Security:** app_settings_get (XML-RPC etc.) / app_vulnerabilities_list / copilot_insights_list / security_get_whitelisted_ips + security_get_whitelisted_ips_mysql / security_suite_server_incidents_list (if suite active)  (SSH-key roster: no list tool; it rides inside `server_get` beside master credentials — UI / direct API for an audit, and record a count)
- [ ] **Manual (UI):** Backup schedule + retention / SSL provider + expiry (no dedicated read tool; the detail rides inside `app_get`, which also returns DB credentials — UI or direct API for an audit) / Additional domains + CNAMEs (the alias tools are all W; the primary domain comes from `app_list`) / SSH-key roster / Cloudflare integration (if any) / WP version (if WP) / Active plugins (if WP)
- [ ] **Document:** Red flags / Recommendations / Quote / SLA
