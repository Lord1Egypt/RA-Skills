# Tools Catalog — Cloudways MCP

The official tool catalog for the **Cloudways (Remote) MCP** (`https://mcp.cloudways.com/mcp/`), taken from the official support articles: [Cloudways MCP Server Tools](https://support.cloudways.com/en/articles/15798823-cloudways-mcp-server-tools) (the dedicated tool reference) and [How to Use Cloudways MCP Server](https://support.cloudways.com/en/articles/14654372-how-to-use-cloudways-mcp-server-for-ai-based-server-management) (setup). Tools appear in Claude as `mcp__cloudways__<tool>` (or `mcp__cloudways-<client>__<tool>` per account).

**MCP v1.2 scale:** **244 tools** — 241 spread across 22 toolsets plus the 3 meta-tools, live-verified 2026-07-20 (see the toolset table below). This matches the [v1.2 announcement](https://www.cloudways.com/blog/cloudways-mcp-v1-2-112-new-tools-role-based-access-tokens-and-full-cloudways-api-coverage/) exactly (112 added in v1.2, covering essentially the full Cloudways API). Your client initially sees only **65 tools** (62 high-frequency direct tools + the 3 meta-tools below). Those 62 are **members of the toolsets**, not a separate tier, so the hidden remainder is **179** (241 − 62) — discovered and invoked on demand through the meta-tools.

> **The official tools article over-lists.** It documents endpoint-style aliases for the Security and Service categories (`security_dns_create`, `service_state_update`, …) plus whole categories — Bot Protection, Client Billing, CloudwaysCDN legacy, a "Lists API", `oauth_access_token_generate` — that **have no live counterpart**. Live re-enumeration on 2026-07-20 found 64 such phantom identifiers and **zero** real alias mismatches: every name in the tables below matches the live `tool_name` exactly. They have been removed from this catalog; if you see them in Cloudways' docs, don't build automation on them.

Flags: **R** = read-only · **W** = write (requires confirmation) · **W!** = destructive / irreversible (requires double confirmation).

> The **live server is the source of truth.** Every section of this file — including the "New in MCP v1.2" half — was reconciled against the live MCP on 2026-07-20 via `list_available_toolsets` + `get_toolset_tools` on a connected account: all 22 toolsets enumerated, every tool name verified byte-for-byte, phantom entries removed. You do **not** need to memorize tool names to use the MCP (it resolves natural language), but knowing them sharpens prompts and lets you confirm an action maps to the tool you expect.
>
> **Most tools are grouped into on-demand toolsets.** Only a subset appears in your default tool list; the rest live inside toolsets (`apps`, `servers`, `git`, `ssh_keys`, `projects`, `staging_management`, `dns_made_easy`, `cloudflare`, and the v1.2 additions) and are invoked through the `execute_tool` proxy. A tool being absent from the default list does **not** mean it is absent from the MCP — `git_*`, `project_*`, `ssh_key_*`, `app_restore_rollback`, `app_db_password_update`, `server_local_backup_delete`, and `staging_app_clone*` are all live via their toolsets (live-verified). Note that `staging_app_clone*` lives in the `apps` toolset, not `staging_management`.
>
> **Toolset descriptions overstate their own contents.** `list_available_toolsets` is reliable for *routing* but not as a capability contract — several descriptions advertise operations that have no tool: `staging_management` (delete latest staging backup — actually `app_local_backup_delete` in `apps`), `security` (install custom SSL — only the *remove* counterpart exists), `cloudways_bot` (list/paginate alerts — only the mark-read tools exist), `copilot` (severity summary, alert-by-id — only `copilot_insights_list`), `agency_os` (disconnect agency, subscribe client to plan, attach/cancel client service, client+service summary, mark invoice paid, reminders — none of the 7 exist). Confirm with `get_toolset_tools` before promising a capability.
>
> There is no `ping` / `customer_info` / `rate_limit_status` tool — verify connectivity with `server_list` and identify the account by the connection prefix.
>
> **Last verified:** 2026-07-20 against the **live MCP** (all 22 toolsets enumerated on a connected account); content sourced from the official v1.2 support articles 2026-07-19. **Note:** three categories are split across the two halves of this file — Cloudflare CDN, Add-on Management, and Copilot each have a pre-v1.2 table above and an "expanded in v1.2" table below; check both.

## Live toolset counts (2026-07-20)

| Toolset | Tools | Toolset | Tools |
|---------|-------|---------|-------|
| `apps` | 52 | `addons` | 10 |
| `servers` | 28 | `dns_made_easy` | 9 |
| `security_suite` | 26 | `monitoring` | 9 |
| `agency_os` | 23 | `copilot` | 9 |
| `cloudflare` | 15 | `cloudways_bot` | 7 |
| `security` | 13 | `services` | 7 |
| `git` | 6 | `projects` | 4 |
| `staging_management` | 5 | `team_member` | 4 |
| `supervisord` | 5 | `ssh_keys` | 3 |
| `app_vulnerability` | 2 | `transfer_server` | 3 |
| `operation` | 1 | `safe_update` | **0** |

**241 toolset tools + 3 meta-tools = 244**, of which 62 toolset members are surfaced directly and the other 179 are on-demand only. `safe_update` is declared by the server but **empty in the current build** — its description states it is "declared but not yet populated", and `execute_tool` returns *"tool not found in toolset"* for anything in it. SafeUpdate (managed WordPress core/plugin/theme updates with visual-regression checks and auto-rollback) is therefore **UI-only** for now; re-check this toolset after future MCP releases.

---

## Server Management

| Tool | Flag | What it does |
|------|------|--------------|
| `server_list` | R | List all servers (status, provider, region, IP, app count). |
| `server_get` | R | Detailed info on one server (hosted apps + configuration). |
| `server_create` | W | Create a server on DigitalOcean/AWS/GCE/Vultr/Linode with an initial app. |
| `server_start` | W | Start a stopped server. |
| `server_stop` | W | Stop a running server. |
| `server_restart` | W | Restart a server to apply configuration changes. |
| `server_delete` | W! | Permanently delete a server and all its data. |
| `server_backup` | W | Create a full backup of a server. |
| `server_scale` | W! | Up/downgrade server size (CPU/RAM) — brief downtime. |
| `server_scale_volume` | W | Change data-volume size (Amazon & GCE only). |
| `server_clone` | W | Clone a server (apps, optionally settings/domains/cron/SSL). |
| `server_update_label` | W | Rename a server. |
| `server_disk_usage_fetch` | W | Initiate a disk-usage fetch operation. |
| `server_snapshot_frequency_update` | W | Configure snapshot frequency (AWS/GCE); empty disables. |
| `server_backup_settings_update` | W | Update backup settings (frequency, retention, off-server/local). |
| `server_local_backup_delete` | W! | Delete local backups stored on the server. |
| `server_package_update` | W! | Install/uninstall/upgrade packages (PHP, MySQL/MariaDB…). Tagged W! because the **uninstall** action removes package data (destructive — double-confirm); install/upgrade are ordinary writes. Discover installable versions via Cloudways' raw `/packages` API endpoint — there is **no** `packages_list` MCP tool (the article's "Lists API" does not exist on the live server). |
| `server_maintenance_window_get` | R | Retrieve maintenance-window settings. |
| `server_maintenance_window_update` | W | Set maintenance window (days + time slot). |
| `server_master_username_update` | W! | Update master username (SSH/SFTP) — the old username stops working immediately. |
| `server_master_password_update` | W! | Update master password (SSH/SFTP). |
| `server_storage_attach` | W | Attach Block Storage volume (DigitalOcean only). |
| `server_storage_scale` | W | Resize Block Storage volume (DigitalOcean only). |
| `operation_status` | R | Check the status of an async operation. |

## Application Management

| Tool | Flag | What it does |
|------|------|--------------|
| `app_list` | R | List all applications on a server. |
| `app_get` | R | Detailed info on one application. |
| `app_create` | W | Create an app (WordPress, Laravel, Magento…). |
| `app_delete` | W! | Permanently delete an app and its data. |
| `app_clone` | W | Clone an app on the same server. |
| `app_clone_to_server` | W | Clone an app to a different server. |
| `staging_app_clone` | W | Clone a staging app on the same server. |
| `staging_app_clone_to_server` | W | Clone a staging app to a different server. |
| `app_backup` | W | Create an application backup. |
| `app_backup_status_get` | R | Status of an in-progress app backup. |
| `app_restore` | W! | Restore an app to a previous backup (local/remote). |
| `app_restore_rollback` | W! | Roll back the last restore (return to pre-restore state). |
| `app_local_backup_delete` | W! | Delete the local backup made during a restore. |
| `app_credentials` | R | Get SSH/SFTP credentials for an app. |
| `app_credentials_create` | W | Create an additional SSH/SFTP credential. |
| `app_credentials_update` | W! | Rename / change password of a credential — the old username/password stop working immediately. |
| `app_credentials_delete` | W! | Delete an access credential. |
| `app_purge_cache` | W | Clear all cache layers (app, Varnish, object). |
| `app_update_label` | W | Rename an application. |
| `app_vulnerabilities_list` | R | List WordPress vulnerabilities with severity scores. |
| `app_vulnerabilities_refresh` | W | Trigger a new vulnerability scan. |
| `app_cname_update` | W | Update the app's primary domain (CNAME). |
| `app_cname_delete` | W! | Delete the CNAME (revert to default Cloudways URL) — removes a customer-facing domain; can break production. |
| `app_aliases_update` | W | Update secondary domains (aliases). |
| `app_cron_list_get` | R | List scheduled cron jobs for an app. |
| `app_cron_list_update` | W | Update the app's cron jobs. **Deprecated on the live MCP** — the underlying `/app/manageCronList` endpoint returns HTTP 500; use `app_cron_optimizer_update` for WP-Cron, or edit the crontab over SSH. |
| `app_cron_optimizer_update` | W | Toggle Cron Optimizer (system cron vs WP-Cron). |
| `app_db_password_update` | W! | Update the app's MySQL/MariaDB password. |
| `app_symlink_update` | W | Change where `public_html` points. |
| `app_webroot_update` | W | Change the webroot (e.g. Laravel `/public_html/public`). |
| `app_cors_headers_update` | W | Update CORS headers. |
| `app_webp_redirection_update` | W | Toggle WebP redirection. |
| `app_enforce_https_update` | W | Toggle HTTPS redirection (force HTTP→HTTPS). |
| `app_reset_permissions` | W | Reset file/folder ownership and modes. |
| `app_fpm_settings_get` | R | Retrieve PHP-FPM configuration. |
| `app_fpm_settings_update` | W | Configure PHP-FPM (workers, children, memory…). |
| `app_varnish_settings_get` | R | Retrieve Varnish config (TTL, paths, exclusions). |
| `app_varnish_settings_update` | W | Update Varnish config. |
| `app_ssh_access_get` | R | Current SSH access status for an app. |
| `app_ssh_access_update` | W | Enable/disable SSH access. |
| `app_access_state_get` | R | Access state (public vs maintenance mode). |
| `app_access_state_update` | W | Set public / maintenance mode. |
| `app_settings_get` | R | Retrieve app setting flags (XML-RPC, GEO-IP, device…). |
| `app_geo_ip_header_update` | W | Toggle the GEO-IP header. |
| `app_xmlrpc_update` | W | Toggle WordPress XML-RPC (off recommended). |
| `app_device_detection_update` | W | Toggle Device Detection (desktop/mobile cache split). |
| `app_ignore_query_string_update` | W | Toggle the Ignore-Query-String cache rule. |
| `app_php_direct_execution_update` | W | Toggle direct PHP execution from uploads (WP security). |
| `app_admin_password_update` | W! | Update the installed app's admin password (e.g. WP admin). |
| `app_password_protection_get` | R | Current HTTP Basic Auth (htpasswd) config. |
| `app_password_protection_update` | W | Enable/update HTTP Basic Auth protection. |
| `app_wp_multisite_update` | W | Enable/update WordPress Multisite. |
| `app_stack_update` | W | Switch stack (v1 Apache hybrid / v2 NGINX lightning). |
| `app_object_cache_update` | W | Toggle WordPress Object Cache (OCP). |

## Service Management

| Tool | Flag | What it does |
|------|------|--------------|
| `service_status` | R | Status of all services on a server. |
| `service_start` | W | Start a stopped service. |
| `service_stop` | W | Stop a running service. |
| `service_restart` | W | Restart a service (nginx, mysql, php-fpm…). |
| `varnish_manage` | W | Enable/disable/purge Varnish at server level. |
| `varnish_app_manage` | W | Enable/disable Varnish per application. |
| `varnish_app_status` | R | Current Varnish status for an application. |

> All 7 are live-verified. The tools article's endpoint-style aliases (`service_state_update`, `service_varnish_manage`, `service_app_varnish_get`) **do not exist** — use the names above.

## Add-on Management

| Tool | Flag | What it does |
|------|------|--------------|
| `addon_list` | R | List available add-ons (status + pricing). |
| `addon_activate` | W | Activate an add-on on the account. |
| `addon_deactivate` | W | Deactivate an account add-on. |
| `addon_activate_on_server` | W | Enable an add-on on a server. |
| `addon_deactivate_on_server` | W | Remove an add-on from a server. |

## Cloudflare CDN

| Tool | Flag | What it does |
|------|------|--------------|
| `cloudflare_add_domain` | W | Add a domain to Cloudflare CDN for an app. |
| `cloudflare_get_details` | R | CDN status, configuration, usage. |
| `cloudflare_get_txt_records` | R | DNS TXT records for domain verification. |

## DNS Made Easy

| Tool | Flag | What it does |
|------|------|--------------|
| `dns_made_easy_list_domains` | R | List managed domains. |
| `dns_made_easy_add_domains` | W | Add domains for DNS management. |
| `dns_made_easy_delete_domains` | W! | Delete domains from DNS Made Easy. |
| `dns_made_easy_get_domain_status` | R | Check domain status. |
| `dns_made_easy_list_records` | R | List DNS records for a domain. |
| `dns_made_easy_add_records` | W | Add DNS records. |
| `dns_made_easy_update_record` | W | Update a DNS record. |
| `dns_made_easy_delete_records` | W! | Delete DNS records. |
| `dns_made_easy_get_domain_usage` | R | DNS usage statistics. |

## Server Settings

| Tool | Flag | What it does |
|------|------|--------------|
| `server_settings_get` | R | View server + PHP configuration. |
| `server_settings_update` | W | Update PHP and MySQL settings. |
| `server_disk_cleanup_settings_get` | R | View disk-cleanup settings. |
| `server_disk_cleanup_settings_update` | W | Configure automated cleanup. |
| `server_disk_cleanup_execute` | W | Run disk cleanup manually. |

## Monitoring & Analytics

| Tool | Flag | What it does |
|------|------|--------------|
| `monitoring_server_summary` | R | Server bandwidth and disk usage. |
| `monitoring_server_usage` | R | Refresh server usage statistics. |
| `monitoring_server_graph` | R | Monitoring graphs (CPU, memory…). |
| `monitoring_app_summary` | R | Application-level usage: `type: bw` for bandwidth, `type: db` for **disk** size (not the database — the live tool's own wording). |
| `analytics_app_traffic` | R | Traffic patterns and sources. |
| `analytics_app_traffic_details` | R | Detailed traffic data for custom ranges. |
| `analytics_app_php` | R | PHP performance / slow pages. |
| `analytics_app_mysql` | R | MySQL queries / performance. |
| `analytics_app_cron` | R | Cron job execution analytics. |

## Copilot Insights

| Tool | Flag | What it does |
|------|------|--------------|
| `copilot_insights_list` | R | Insights, alerts, and recommendations for your infrastructure. |

## Projects

| Tool | Flag | What it does |
|------|------|--------------|
| `project_list` | R | List Projects (IDs, names, grouped servers/apps). |
| `project_create` | W | Create a Project with initial app members. |
| `project_update` | W | Rename / change a Project's members. |
| `project_delete` | W! | Delete a Project (grouping only; resources untouched). |

## Git Deployment

| Tool | Flag | What it does |
|------|------|--------------|
| `git_generate_key` | W! | Generate a fresh SSH deploy key for an app — overwrites the previous deploy key, which stops working until the new public half is re-registered on the Git host. |
| `git_key_get` | R | Retrieve the public deploy key (paste into GitHub/GitLab/Bitbucket). |
| `git_branches_get` | R | Refresh/list branches in the linked repo. |
| `git_clone` | W | Clone a repo/branch into the web root (initial link). |
| `git_pull` | W | Pull latest commits and deploy. |
| `git_history_get` | R | Recent deployment history (commit hashes, status). |

## SSH Key Management

| Tool | Flag | What it does |
|------|------|--------------|
| `ssh_key_create` | W | Add an SSH public key to a server/app/user. |
| `ssh_key_update` | W | Rename an SSH key (label only). |
| `ssh_key_delete` | W! | Revoke an SSH key by `ssh_key_id`. |

## Toolset meta-tools

The server also exposes discovery/proxy tools for navigating its toolsets. Usually you call the named tools above directly; these are for when the client groups tools into on-demand toolsets.

| Tool | Flag | What it does |
|------|------|--------------|
| `list_available_toolsets` | R | List the server's toolsets (categories of tools). |
| `get_toolset_tools` | R | List the tools inside a given toolset. |
| `execute_tool` | varies | Invoke a tool by name through the proxy (inherits that tool's R/W/W! risk). |

---

# New in MCP v1.2 (2026-07)

Everything below was added in Cloudways MCP v1.2 and is documented in the [official tools article](https://support.cloudways.com/en/articles/15798823-cloudways-mcp-server-tools). These categories **close the gaps this catalog previously flagged as "UI/direct-API only"**: SSL / Let's Encrypt, SSH/MySQL/Adminer/Web-SSH IP whitelisting, and team-member management are now MCP tools. Most of these live in on-demand toolsets (invoked via `execute_tool`); R/W/W! risk tags below are this skill's operational assessment, not Cloudways labels.

## Security — SSL & IP Access (new in v1.2)

| Tool | Flag | What it does |
|------|------|--------------|
| `security_lets_encrypt_install` | W | Provision + install a Let's Encrypt SSL cert on an app (HTTP-01 or DNS-01 challenge). |
| `security_lets_encrypt_renew` | W | Force an out-of-cycle renewal of an existing Let's Encrypt cert. |
| `security_lets_encrypt_revoke` | W! | Revoke a Let's Encrypt cert — HTTPS falls back to no SSL (breaks production HTTPS). |
| `security_lets_encrypt_auto_renewal` | W | Toggle Let's Encrypt auto-renewal on/off for an app. |
| `security_remove_own_ssl` | W! | Remove a previously-installed custom (own) SSL cert from an app. |
| `security_create_dns` | W | Create the DNS challenge (TXT) record required to issue a wildcard SSL cert. |
| `security_verify_dns` | W | Verify the published DNS challenge record so the wildcard cert can be issued. |
| `security_get_whitelisted_ips` | R | List IPs whitelisted for SSH/SFTP access on a server. |
| `security_get_whitelisted_ips_mysql` | R | List IPs whitelisted for remote MySQL access. |
| `security_update_whitelisted_ips` | W! | **Replace** the SSH/SFTP or MySQL IP whitelist — overrides the current list; a wrong list can lock you (or the client) out. Always read the current list first. |
| `security_check_blacklisted_ip` | R | Check whether an IP is blacklisted on the server. |
| `security_whitelist_ip_siab` | W | Whitelist an IP for Shell-in-a-Box (browser Web SSH). |
| `security_whitelist_ip_adminer` | W | Whitelist an IP for Adminer (browser DB manager). |

> **13 tools, all live-verified.** The tools article lists endpoint-style aliases for several of these (`security_dns_create`, `security_dns_verify`, `security_lets_encrypt_auto_renewal_update`, `security_mysql_whitelisted_ips_get`, `security_ssh_sftp_whitelisted_ips_get`, `security_whitelisted_ips_update`, `security_ip_blacklist_check`, `security_adminer_allow`, `security_siab_allow`) plus CSR tools (`security_csr_create` / `security_csr_get`) — **none of them exist on the live server.** The names in the table are the real ones.
>
> There is **no tool to install a custom SSL cert** (only `security_remove_own_ssl` to remove one), despite the toolset description claiming otherwise — the install/paste step is UI or direct-API only.

## Security Suite — Anti-Malware / WAF (new in v1.2)

| Tool | Flag | What it does |
|------|------|--------------|
| `security_suite_app_activate` | W | Enroll an app in the Security Suite (anti-malware, WAF, firewall). |
| `security_suite_app_deactivate` | W | Unenroll an app from the Security Suite (removes protection). |
| `security_suite_app_status_get` | R | Suite status for an app (active/inactive, last scan, threat count, tier). |
| `security_suite_app_scans_list` | R | List all scans performed on an app. |
| `security_suite_app_scan_start` | W | Start an on-demand malware / file-integrity scan. |
| `security_suite_app_scan_status_get` | R | Status of ongoing/recent scans (queued/running/completed/failed). |
| `security_suite_app_scan_details_get` | R | Detailed per-file findings for a scan. |
| `security_suite_app_files_list` | R | List monitored / quarantined / affected files on an app. |
| `security_suite_app_files_restore` | W! | Restore quarantined files — **can put malware back on the live site**; inspect the cleaned-vs-infected diff first. |
| `security_suite_app_files_cleaned_diff_get` | R | Side-by-side cleaned-vs-infected file comparison. |
| `security_suite_app_events_list` | R | Recent security events for an app (audit feed). |
| `security_suite_app_incidents_list` | R | Detected incidents for an app (correlated events). |
| `security_suite_app_ips_update` | W | Add/update IPs in the app's allowlist or blocklist. |
| `security_suite_app_ips_delete` | W | Delete IPs from the app's allowlist or blocklist. |
| `security_suite_server_incidents_list` | R | Incidents at server level (all apps). |
| `security_suite_server_stats_get` | R | Server-level suite stats (threats, WAF alerts, brute-force, etc.). |
| `security_suite_server_apps_list` | R | Which apps on a server are enrolled / unprotected. |
| `security_suite_server_ips_get` | R | Server-level allowlist/blocklist IPs. |
| `security_suite_server_ips_update` | W | Add/update server-level allowlist/blocklist IPs (affects every app). |
| `security_suite_server_ips_delete` | W | Delete server-level allowlist/blocklist IPs. |
| `security_suite_server_countries_blacklist_update` | W! | Block **all traffic** from selected countries (ISO codes) — server-wide traffic impact. |
| `security_suite_server_countries_blacklist_delete` | W | Lift a country-level block. |
| `security_suite_server_infected_domains_list` | R | Infected/compromised domains detected on a server. |
| `security_suite_server_infected_domains_sync` | W | Force a re-sync of the infected-domains list. |
| `security_suite_server_firewall_settings_get` | R | Current firewall config (rule sets, thresholds, geo-blocking). |
| `security_suite_server_firewall_settings_update` | W | Update firewall config (rule sets, thresholds, geo-blocking). |

## CloudwaysBot — Alerts & Integrations (new in v1.2)

| Tool | Flag | What it does |
|------|------|--------------|
| `cloudways_bot_alert_mark_read` | W | Acknowledge one alert by `alert_id`. |
| `cloudways_bot_alerts_mark_all_read` | W | Bulk-acknowledge all unread alerts. |
| `cloudways_bot_integrations_list` | R | List configured alert channels (Slack, email, webhooks) + rules. |
| `cloudways_bot_integration_channels_list` | R | Catalogue of supported channel types + event types. |
| `cloudways_bot_integration_create` | W | Create a new alert channel. |
| `cloudways_bot_integration_update` | W | Update an alert channel's rules/recipients/URL. |
| `cloudways_bot_integration_delete` | W! | Delete an alert channel — alerts silently stop being delivered there. |

## Staging Management (new in v1.2)

| Tool | Flag | What it does |
|------|------|--------------|
| `staging_sync_tables` | W! | Sync/refresh database tables between staging and production — overwrites the target's data. |
| `staging_sync_code` | W! | Sync code and/or DB between staging and deployed production (push to live or pull to staging) — a wrong direction overwrites production. Confirm **direction** explicitly. |
| `staging_auth_status_update` | W | Enable/disable htaccess (Basic Auth) on a staging app. |
| `staging_htaccess_update` | W | Update the staging app's htaccess credentials. |
| `staging_logs_get` | R | Recent staging operation logs (syncs, refreshes, backups). |

## Team Members (new in v1.2)

| Tool | Flag | What it does |
|------|------|--------------|
| `team_member_list` | R | List sub-users with their roles and server/app access. |
| `team_member_add` | W | Invite a new team member (email, role, access set). |
| `team_member_update` | W! | Change a member's role or access — an over-grant is a security event; confirm the exact access set. |
| `team_member_delete` | W! | Revoke a member's access to the account. |

## Server Transfer (new in v1.2)

| Tool | Flag | What it does |
|------|------|--------------|
| `server_transfer_request` | W! | Hand a server's **ownership** to another Cloudways account — after acceptance the server leaves this account entirely. |
| `server_transfer_status_get` | R | Status of an in-flight transfer (pending/accepted/completed/cancelled/rejected). |
| `server_transfer_cancel` | W | Cancel a not-yet-accepted transfer. |

## Supervisord — Queues / Workers (new in v1.2)

| Tool | Flag | What it does |
|------|------|--------------|
| `supervisord_list_queues` | R | List Supervisord-managed worker queues for an app (config included). |
| `supervisord_queue_status` | R | Runtime status of the app's queues (running/stopped/fatal, pid, uptime). |
| `supervisord_create_queue` | W | Create a worker queue (connection, procs, sleep, artisan path, …). |
| `supervisord_restart_queue` | W | Restart a queue's workers (e.g. after a deploy). |
| `supervisord_delete_queue` | W! | Delete a queue — stops its workers and removes the definition. |

## Copilot — Subscription & Settings (expanded in v1.2)

`copilot_insights_list` (R, above) existed before; the rest are new:

| Tool | Flag | What it does |
|------|------|--------------|
| `copilot_plans_list` | R | Available Copilot plans and prices. |
| `copilot_subscription_status` | R | Current subscription (plan, renewal, active/inactive). |
| `copilot_billing_get` | R | Real-time Copilot billing/usage for the cycle. |
| `copilot_subscribe` | W | Subscribe to a Copilot plan — **incurs cost**. |
| `copilot_plan_change` | W | Upgrade/downgrade the Copilot plan — changes cost. |
| `copilot_unsubscribe` | W! | Cancel the Copilot subscription. |
| `copilot_server_settings_get` | R | Per-server Copilot settings (lists only servers where Copilot was disabled). |
| `copilot_server_settings_update` | W | Toggle Copilot per server / adjust thresholds. |

## AgencyOS (new in v1.2)

| Tool | Flag | What it does |
|------|------|--------------|
| `agency_os_agency_create` | W | Create an AgencyOS agency (Stripe link optional, can be added later). |
| `agency_os_agency_list` | R | List agencies under the account. |
| `agency_os_client_create` / `agency_os_client_update` | W | Create / update an agency client record. |
| `agency_os_client_list` / `agency_os_client_get` | R | List clients / client details. |
| `agency_os_client_delete` | W! | Delete a client — cancels/archives their services and invoice history. |
| `agency_os_service_create` / `agency_os_service_update` | W | Create / edit a service offering. |
| `agency_os_service_list` / `agency_os_service_get` | R | List services / details. |
| `agency_os_plan_price_create` | W | Attach a price plan to a service. |
| `agency_os_plan_price_list` / `agency_os_plan_price_get` | R | List / get price plans. |
| `agency_os_plan_update` | W | Rename / activate / deactivate a plan. |
| `agency_os_client_subscriptions_get` | R | Services attached to a client. |
| `agency_os_client_invoices_list` / `agency_os_invoices_list` | R | Client / agency-wide invoices. |
| `agency_os_tax_rate_create` | W | Create a tax rate. |
| `agency_os_tax_rate_list` | R | List tax rates. |
| `agency_os_country_specs_get` | R | Supported countries + ISO codes (reference data). |
| `agency_os_reports_list` | R | Client/service reports. |
| `agency_os_report_archive` | W | Archive/unarchive a report. |

## Cloudflare CDN — expanded in v1.2

The three tools above (`cloudflare_add_domain`, `cloudflare_get_details`, `cloudflare_get_txt_records`) existed before; v1.2 adds:

| Tool | Flag | What it does |
|------|------|--------------|
| `cloudflare_delete_domain` | W! | Offboard a domain from Cloudflare CDN — proxying stops; can break production behavior. |
| `cloudflare_transfer_domain` | W | Move a domain's CDN attachment between apps in the same account. |
| `cloudflare_purge_domain` | W | Purge the Cloudflare edge cache for a domain. |
| `cloudflare_get_dns_query` | R | Cloudflare DNS verification status for a domain. |
| `cloudflare_verify_txt_records` | W | Trigger an immediate re-check of the published TXT records. |
| `cloudflare_get_fpc_status` | R | Smart Cache Purge (FPC) deployment status. |
| `cloudflare_deploy_fpc` | W | Configure/deploy Smart Cache Purge for a domain. |
| `cloudflare_get_settings` | R | Per-domain Cloudflare settings (caching, minify, image optimization, …). |
| `cloudflare_get_analytics` | R | Cache analytics (hit rate, bandwidth saved, edge requests). |
| `cloudflare_get_security_analytics` | R | Security analytics (threats blocked, WAF events, bot mitigation). |
| `cloudflare_get_logpush_analytics` | R | Raw Logpush request-log analytics. |
| `cloudflare_get_logpush_security` | R | Raw Logpush security-event data. |

## Add-on Management — expanded in v1.2

In addition to the five `addon_*` tools above:

| Tool | Flag | What it does |
|------|------|--------------|
| `addon_upgrade` | W | Upgrade an activated add-on to a higher-tier package — changes cost. |
| `addon_request` | W | Submit a per-app add-on request (for add-ons provisioned per application). |
| `addon_elastic_list_domains` | R | List Elastic Email sender domains. |
| `addon_elastic_verify_domain` | W | Verify a sender domain's DNS in Elastic Email. |
| `addon_elastic_delete_domain` | W! | Delete a sender domain from Elastic Email — mail from that domain stops sending. |

---

## Still not exposed (use UI or direct API)

- **SSH-key listing** — keys are managed via `ssh_key_create`/`ssh_key_update`/`ssh_key_delete`, but there is no dedicated read/list tool. Key metadata **does** come back inside the `server_get` payload — along with that server's **master credentials**, which is why an audit should read the roster in the Cloudways UI (Server → Security) or via the direct API and record a count. Reach for `server_get` when you need the metadata for one specific server and accept what comes with it (safety rule 7).
- **SafeUpdate (managed WordPress updates)** — the `safe_update` toolset is declared but empty in the current build (0 tools); scheduling, run-now, history, and auto-rollback are UI-only.
- **Custom SSL install** — `security_remove_own_ssl` removes a custom cert, but there is no install counterpart; paste the cert in the UI or use the direct API.
- **Bot Protection, Client Billing, CloudwaysCDN (legacy), reference-data "Lists API", OAuth token minting** — documented in Cloudways' tools article but **absent from the live MCP**; UI or direct API only.
- **Backup listing** — `app_backup_status_get` reports only an in-progress backup; available restore points are visible in the UI.
- **Account/plan info** — no `customer_info` tool; plan/billing status of the Cloudways account itself is UI-only.
