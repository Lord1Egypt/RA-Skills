# Tools Catalog — Cloudways MCP

The official tool catalog for the **Cloudways (Remote) MCP** (`https://mcp.cloudways.com/mcp/`), taken from the [official support article](https://support.cloudways.com/en/articles/14654372-how-to-use-cloudways-mcp-server-for-ai-based-server-management). Tools appear in Claude as `mcp__cloudways__<tool>` (or `mcp__cloudways-<client>__<tool>` per account).

Flags: **R** = read-only · **W** = write (requires confirmation) · **W!** = destructive / irreversible (requires double confirmation).

> The **live server is the source of truth.** Names below match the article, but always check the actual `mcp__cloudways*__*` tools connected in Claude — capabilities evolve. You do **not** need to memorize tool names to use the MCP (it resolves natural language), but knowing them sharpens prompts and lets you confirm an action maps to the tool you expect.

> ⚠️ **Not exposed by the official MCP** (per the article): **SSL / Let's Encrypt**, **SSH/MySQL IP whitelisting**, and **team-member management** have **no MCP tool**. Do those in the Cloudways Platform UI or via the [direct Cloudways API](https://developers.cloudways.com/). There is also no `ping` / `customer_info` / `rate_limit_status` tool — verify connectivity with `server_list` and identify the account by the connection prefix.

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
| `server_package_update` | W | Install/uninstall/upgrade packages (PHP, MySQL/MariaDB…). |
| `server_packages` | R | Discover available packages for a server. |
| `server_maintenance_window_get` | R | Retrieve maintenance-window settings. |
| `server_maintenance_window_update` | W | Set maintenance window (days + time slot). |
| `server_master_username_update` | W | Update master username (SSH/SFTP). |
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
| `app_credentials_update` | W | Rename / change password of a credential. |
| `app_credentials_delete` | W! | Delete an access credential. |
| `app_purge_cache` | W | Clear all cache layers (app, Varnish, object). |
| `app_update_label` | W | Rename an application. |
| `app_vulnerabilities_list` | R | List WordPress vulnerabilities with severity scores. |
| `app_vulnerabilities_refresh` | W | Trigger a new vulnerability scan. |
| `app_cname_update` | W | Update the app's primary domain (CNAME). |
| `app_cname_delete` | W | Delete the CNAME (revert to default Cloudways URL). |
| `app_aliases_update` | W | Update secondary domains (aliases). |
| `app_cron_list_get` | R | List scheduled cron jobs for an app. |
| `app_cron_list_update` | W | Update the app's cron jobs. |
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
| `monitoring_app_summary` | R | Application-level usage metrics. |
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
| `git_generate_key` | W | Generate a fresh SSH deploy key for an app. |
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

## Not available as MCP tools (use UI or direct API)

Per the official article, the MCP does **not** expose these — handle them in the Cloudways Platform or via the [direct API](https://developers.cloudways.com/):

- **SSL / Let's Encrypt** — install/renew/revoke certificates.
- **SSH / MySQL IP whitelisting** — add/remove allowed IPs.
- **Team-member management** — invite/manage users.

When a task needs one of these, say so plainly and point to the UI/API rather than guessing a tool.
