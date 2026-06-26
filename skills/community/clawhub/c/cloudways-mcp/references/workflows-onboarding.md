# Workflows — Onboarding & Audit (agency client takeover)

Core scenario: a new client arrives with a site on Cloudways, and you need to build a complete picture — no crashes, no surprises at 3 AM.

> **Guiding principle:** On the first audit, **don't touch anything.** Just read. Full documentation of the current state first. Changes come after you understand the picture and have a structured plan.

---

## Stage 0 — Pre-flight (before calling MCP)

Confirm with the client:
- [ ] API access approved on their side
- [ ] New API key (don't share with their old team)
- [ ] If there are old team members who don't need access — add this at this point (not via MCP — UI only)

---

## Stage 1 — Account mapping

```
1. server_list                 → all servers: count, providers, regions, sizes (this is the entry point — infer the account from the connection prefix; there is no whoami/customer_info tool)
2. project_list                → how they're organized
3. copilot_insights_list       → insights, alerts, and recommendations currently open
```

> **No MCP tool for:** account/plan/billing status (`customer_info`), team-member roster (`list_team_members`), or SSH-key listing. Plan/billing and the team roster are checked in the Cloudways Platform UI; SSH keys are managed via `ssh_key_create` / `ssh_key_update` / `ssh_key_delete` but there is no read/list tool — confirm SSH access in the UI or via the direct Cloudways API (<https://developers.cloudways.com/>).

**Deliverables you record:**

| Field | Value |
|------|-----|
| Cloudways plan | (Starter/Growth/Enterprise? — UI only) |
| Number of servers | |
| Providers in use | (DO/AWS/GCP/Vultr) |
| Regions | |
| Total monthly $ Cloudways (estimate) | |
| Team members + permissions | (UI only) |
| SSH keys (don't publish — only a count) | (UI / direct API) |
| Open insights/alerts | (copilot_insights_list) |

---

## Stage 2 — Server mapping

For each server in the list:

```
1. server_get                  → label, size, IP, master credentials, app list
2. server_settings_get         → PHP timeout, memory, upload limit, custom PHP
3. service_status              → what's running (Apache/Nginx/MySQL/Memcached/Varnish/Redis)
4. server_disk_usage_fetch     → trigger a fresh disk-usage calculation (init), then:
5. monitoring_server_summary   → current disk + bandwidth usage (read)
6. monitoring_server_graph     → CPU/RAM trends last 24h
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

For each application (per the app list from the previous stage):

```
1. app_get                     → URL, FQDN, app folder, DB credentials
2. app_settings_get            → app-level overrides + security flags (XML-RPC, password protection, etc.)
3. app_credentials             → SFTP/additional access
4. monitoring_app_summary      → bandwidth, requests (to get a sense of scale)
5. analytics_app_traffic       → visitors at least last 7 days (drill in with analytics_app_traffic_details)
6. analytics_app_php           → slow scripts? memory issues?
7. analytics_app_mysql         → slow queries?
8. app_varnish_settings_get    → cache configured?
9. app_vulnerabilities_list    → (WordPress) known plugin/theme/core vulnerabilities
```

> **SSL status is not exposed by an MCP tool.** Check certificate provider + expiry in the Cloudways Platform UI or via the direct Cloudways API.

**Deliverables table for each app:**

| Field | Value | red flag? |
|------|-----|-----------|
| App name | | |
| Primary domain | | |
| Additional domains/CNAMEs | | |
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
1. app_settings_get            → per-app security flags (XML-RPC enabled? password protection?)
2. app_vulnerabilities_list    → (WordPress) open plugin/theme/core vulnerabilities
3. copilot_insights_list       → security-related insights/recommendations Cloudways has surfaced
```

> **No MCP tools for IP whitelisting or SSH-key listing.** The SSH IP whitelist, MySQL IP whitelist, and the stored-SSH-key roster are **not** exposed by the official Cloudways MCP. Audit these in the Cloudways Platform UI (Server → Security) or via the direct Cloudways API (<https://developers.cloudways.com/>). The same goes for the team-member roster (who still has access) — UI / API only.

**Red flags (check in the UI / API):**
- [ ] SSH whitelist empty = open to the world (critical)
- [ ] MySQL whitelist empty = open to the world (security disaster)
- [ ] Old SSH keys whose owners are unclear
- [ ] The old team member still has access
- [ ] Access not only for client employees but also for employees who have left

**Red flags (from MCP):**
- [ ] XML-RPC left enabled on WordPress (`app_settings_get`) = brute-force/DDoS vector
- [ ] Open vulnerabilities reported by `app_vulnerabilities_list`

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

- [ ] **Account:** server_list / project_list / copilot_insights_list  (plan/billing + team roster = UI only)
- [ ] **Per server:** server_get / server_settings_get / service_status / server_disk_usage_fetch + monitoring_server_summary / monitoring_server_graph
- [ ] **Per app:** app_get / app_settings_get / monitoring_app_summary / analytics_app_traffic / analytics_app_php / analytics_app_mysql / app_varnish_settings_get / app_vulnerabilities_list (WP)
- [ ] **Security:** app_settings_get (XML-RPC etc.) / app_vulnerabilities_list / copilot_insights_list  (IP whitelists + SSH-key roster = UI / API only)
- [ ] **Manual (UI):** Backup schedule + retention / SSL provider + expiry / IP whitelists / SSH-key roster / team members / Cloudflare integration (if any) / WP version (if WP) / Active plugins (if WP)
- [ ] **Document:** Red flags / Recommendations / Quote / SLA
