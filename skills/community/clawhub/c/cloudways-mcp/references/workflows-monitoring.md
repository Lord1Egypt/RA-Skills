# Workflows — Monitoring (read-only)

Monitoring scenarios only. None of the actions here require confirmation — they are all read.

> **Basic rule:** Before reporting to the user that something is wrong, gather enough data to be sure. A report with a single data point is noise — a report with 3-4 data points that all point to the same thing is a signal.

---

## 1. Daily account status snapshot

**When:** "Show me what's going on / general overview / what's the situation today"

**Call sequence:**

1. `server_list` — list + status for each server (also confirms the account/connection is reachable; there is no separate account-info tool)
2. `copilot_insights_list` — what's open right now
3. For each server with a status other than Running: `server_get` to check why

**How to summarize:**
- How many servers, how many apps, how many active / inactive
- Open alerts — by severity
- If everything is clean: "All systems operational, X servers, Y apps, no open alerts"
- Don't pad with text if everything is fine — be concise

---

## 2. Health check before a significant change

**When:** Before deployment / migration / DNS change / confirming a significant change for the client

**Goal:** baseline before, baseline after. If something goes wrong, you'll have a point of comparison.

**Call sequence:**

1. `server_get` (the target server) — current state
2. `monitoring_server_graph` — CPU, RAM, disk I/O over the last 5 minutes
3. `service_status` — verify all the services are running
4. `monitoring_server_summary` — free space (run `server_disk_usage_fetch` first to initialize the data, then read with `monitoring_server_summary`)
5. `monitoring_app_summary` (for each relevant application) — bandwidth, response time
6. `copilot_insights_list` — no active surprises
7. `analytics_app_traffic` (last 24h) — to know what the normal traffic is

**Save the output before starting the change.** After the change, repeat the same sequence and compare.

---

## 3. Disk usage investigation

**When:** disk space alert, or "the server is slow"

**Sequence:**

1. `server_disk_usage_fetch` (init) then `monitoring_server_summary` (read) — where is the space?
2. If application folders are large: for each suspect app `app_get` + `app_settings_get`
3. Check logs via manual SSH (Cloudways MCP does not expose direct file system access): the administrator will need to connect via SSH to `/var/log/`, `/home/master/applications/<app>/logs/`
4. Check MySQL slow logs: `analytics_app_mysql` — if there are a lot of slow queries, the bin logs can balloon

**Good report:**
```
Server prod-shop-il (1234567): disk 87% full
Breakdown:
  - /home/master/applications/woocommerce-prod/public_html: 18GB
  - /var/log: 4.2GB (30 days of logs — rotation possible)
  - /tmp: 2.1GB
  - other: 6GB
Recommendation: app_purge_cache for all apps + manual log rotation via SSH
Next action requires confirmation: app_purge_cache (W)
```

---

## 4. Performance investigation — "the site is slow"

**When:** a client complains about slowness

**Step 1 — Is it really slow, or just their perception?**

1. `analytics_app_traffic` (last hour) — basically, traffic spike?
2. `monitoring_app_summary` — response time avg + p95
3. `monitoring_server_graph` — CPU/RAM of the server overall

**Step 2 — Where is the problem?**

1. `analytics_app_php` — slow scripts? memory exhaustion?
2. `analytics_app_mysql` — slow queries? locks?
3. `service_status` — Varnish/Memcached/Redis running?
4. `app_varnish_settings_get` — cache mode configured?

**Diagnostic matrix:**

| Symptom | Likely cause | Diagnostic tool |
|--------|----------|-----------|
| Sustained CPU 100% | PHP heavy / DB heavy | `analytics_app_php` + `analytics_app_mysql` |
| RAM 95%+ | memory leak / cache bloat | `service_status` + restart services |
| High Disk I/O | swap / log writes / DB writes | `server_disk_usage_fetch` (init) + `monitoring_server_summary` (read) |
| High response time but reasonable CPU/RAM | Varnish not running / slow external API | `service_status` + `app_varnish_settings_get` |
| Traffic spike | DDoS / viral / bot | `analytics_app_traffic` (sources) |

---

## 5. SSL expiry monitoring

**When:** weekly review of clients' SSL expiry dates

**Sequence for each application:**

1. `server_list`
2. For each server: `server_get` → list of apps
3. For each app: `app_get` → inspect the SSL/expiry detail returned for the app
4. Filter: SSL expiring within the next 30 days → flag for renewal
5. For each flagged app: confirm whether Let's Encrypt auto-renewal is enabled. SSL status and auto-renewal are not exposed as MCP tools — verify (and renew/configure) in the Cloudways Platform UI or via the direct Cloudways API (https://developers.cloudways.com/). If auto-renewal is off — double flag.

> If Let's Encrypt auto-renewal is active, Cloudways renews 30 days before expiry. If it fails to renew (DNS issue) — you'll get an alert. It's still worth reviewing manually once every two weeks. Note: SSL install/renew/revoke and auto-renewal are not MCP tools — handle them in the Cloudways UI or the direct API.

---

## 6. Traffic anomaly detection

**When:** "there's a jump in traffic" / "sales dropped" / before a campaign

**Sequence:**

1. `analytics_app_traffic` — bottom line: visitors, pageviews
2. If a spike: source of the traffic? geographic distribution? (`analytics_app_traffic_details`)
3. Compare to the same day in the previous week / previous month
4. If a drop: `monitoring_app_summary` — did the error rate go up?
5. Check `copilot_insights_list` — maybe something is taking the site down

> Cloudways analytics do not replace GA4/Plausible. They complement them with server-level metrics (raw bandwidth, requests). The two angles together give a good picture.

---

## 7. Multi-server comparison

**When:** "which server is client X on?" / "comparison between production and staging"

**Sequence:**

1. `server_list` — filter by label/project
2. For two or three servers: `server_get` + `monitoring_server_graph` in parallel
3. Compare: provider, region, size, RAM/CPU usage, applications

**Tip:** Cloudways sometimes groups one client's apps on the same server. This can be a problem in production: a spike in one application affects the others. In an audit for a new client, this is the first thing to check.
