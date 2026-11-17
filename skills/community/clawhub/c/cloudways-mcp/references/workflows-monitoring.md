# Workflows — Monitoring (read-only)

Monitoring scenarios only. Almost everything here is read-only and needs no confirmation. One exception: `server_disk_usage_fetch` is classified **W** (it triggers a fresh disk-usage calculation), so per the skill's rule it **still requires a quick confirmation** before running — no local carve-outs from the every-W-confirms invariant. Default to the cached values `monitoring_server_summary` already returns; confirm-and-fetch only when the user needs fresh numbers (and note the fetch may be blocked on a READ token — fall back to cached data if so).

> **Basic rule:** Before reporting to the user that something is wrong, gather enough data to be sure. A report with a single data point is noise — a report with 3-4 data points that all point to the same thing is a signal.

---

## 1. Daily account status snapshot

**When:** "Show me what's going on / general overview / what's the situation today"

**Call sequence:**

1. `server_list` — list + status for each server (also confirms the account/connection is reachable; there is no separate account-info tool)
2. `copilot_insights_list` — what's open right now
3. For each server with a status other than Running: `service_status` (what is down) and the
   insights from step 2 that name that server — the two things "why" usually is. If you hold an
   operation id from an earlier write in this conversation (a restart, a scale, a backup),
   `operation_status` on **that id** says whether it is still in flight; it takes an operation
   id, not a server id, so there is nothing to ask it for a server that simply stopped.
   `server_get` would add the server's master credentials to an answer that needs none of this.

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

1. The target server's row — status, size, provider, region, IP, app **count** (the app
   *roster* is step 2; the row does not carry app ids). That is the "current state" a baseline
   records. **Nothing below needs it to run**: steps 3–5 take the `server_id`, steps 6 and 8
   take the `(server_id, app_id)` pair, and the ids are what you already have. So for an
   **app-scoped** change with a known pair, proceed from the ids; if the descriptive fields
   are wanted in the record, take them from the `server_list` response you **already hold**
   from this conversation (zero calls) or from the server's page in the Cloudways UI — and
   never from `server_get`, which would import the server's **master credentials** *and* every
   hosted application's row (rule 7: may carry each application's database credentials) for
   a row no later step reads. That is the exact roster step 2 refuses to fetch for this case,
   plus the master credentials on top. For a **server-wide** change the ladder is: the held
   `server_list` response; else the UI page; else, if it must be the API from here, **one
   `server_get` for that server** — knowing its full scope as just stated, and knowing it
   also supplies the step-2 roster, so step 2 then makes no `app_list` call. Narrower than an
   account-wide `server_list`, wider than "one credential" — which is why the UI page is the
   better rung. Do **not** call `server_list` to pick one row you know the id of: rule 7
   describes its payload, and it covers every server in the account, so it exposes strictly
   more than the `server_get` it would be standing in for. `server_list` is for the fleet
   question, not the single-server one.
2. The roster — **only if the change is server-wide.** If the significant change is scoped
   to one application whose `(server_id, app_id)` you already know, steps 6 and 8 take that id
   and nothing else: **make no roster call**, since `app_list` would import every application's
   row (credentials included, per rule 7) for no benefit. For a server-wide baseline —
   a PHP upgrade, a migration, a DNS change affecting every site — you need every app id:
   the roster you already hold from this conversation (a step-1 `server_get`, if one was
   made, already returned it), else one `app_list` on that server
   (`server_list` gives a *count*; `monitoring_app_summary` / `analytics_app_traffic` take an
   app id beside the server id; `server_get` used to supply this roster implicitly, beside
   the master credentials). One call, whose payload rule 7 describes.
3. `monitoring_server_graph` — CPU, RAM, disk I/O over the last 5 minutes
4. `service_status` — verify all the services are running
5. `monitoring_server_summary` — free space (run `server_disk_usage_fetch` first to initialize the data, then read with `monitoring_server_summary`)
6. `monitoring_app_summary` — bandwidth, response time — for the **known target app** when the
   change is app-scoped (its `(server_id, app_id)` is the id step 2 said to use, and there is
   no roster), or for each application in the step-2 roster when the change is server-wide
7. `copilot_insights_list` — no active surprises
8. `analytics_app_traffic` (last 24h) — to know what the normal traffic is — for the same
   application set as step 6: the known target app, or the step-2 roster

**Save the output before starting the change.** After the change, repeat the same sequence and compare.

---

## 3. Disk usage investigation

**When:** disk space alert, or "the server is slow"

**Sequence:**

1. `server_disk_usage_fetch` (init) then `monitoring_server_summary` (read) — where is the space?
2. If application folders are large, you need the roster, and the roster is what costs you:
   the one you **already hold** from this conversation (zero calls); else an externally
   filtered roster (the server's Applications tab in the UI, or a direct `GET /server` through
   a field filter) when the attribution has to stay credential-free; else one `app_list` —
   `server_list` returns only an app count — whose payload rule 7 describes: every app on the
   server, credentials included per the live tool's own description. Then
   `monitoring_app_summary` (`type: db`) per app for its **disk** size — the live tool
   describes its two types as `bw` for bandwidth and `db` for disk size; `db` is not the
   database, and a media-heavy site with a small database is exactly the case where reading
   it as one would misattribute. The size calls add nothing on top of what the roster cost;
   that is the only sense in which this pass is clean. The breakdown from step 1 names **folders**
   (`/home/master/applications/<folder>/`), and the folder name is a field `app_get` returns
   and nothing else does. Usually the disk sizes settle it: the largest folder belongs to the
   app whose `type: db` figure is the largest — with the caveat that this figure is the application's storage as Cloudways
   accounts it, which has not been verified here to equal the folder byte-for-byte, so treat a
   near-tie as a tie. When they do not settle it — two or three apps of similar size — the folder name
   has to be read for **those candidates only**: from each one's page in the Cloudways UI
   (nothing enters the transcript), or with `app_get` on each candidate, which is the rule-7
   case of a specific field nothing else returns, accepting the database credentials that come
   with each call. The candidate set is bounded by the size ranking, never the whole server.
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

**A fleet-wide sweep does not run through the agent.** Certificate provider and expiry come
back only inside `app_get`, which returns that application's **database credentials** in the
same payload. Looping it over every app therefore pulls every app's DB password into the
transcript to learn a date — the credentials are not needed for the question being asked, and
once fetched they cannot be taken back out. Earlier versions of this playbook authorized that
loop under conditions; they should not have. Collect the dates **outside the conversation**:

- the Cloudways Platform UI (Application → SSL Certificate), or
- a direct `GET /server` / app call piped through a field filter on your side, so only
  `label`, `app_fqdn` and the certificate fields come back. `workflows-automation.md`
  § “SSL expiry monitoring” already runs exactly this as a Sunday cron, outside any agent
  session — that is the collector this step wants. It must be a **script**, not a headless
  agent: an agent asked for expiry dates has only `app_get` to get them with, which is the
  sweep this section exists to prevent.

Then bring the resulting list — names and dates, no payloads — to the agent for the triage
below. **In the agent, `app_get` is for one certificate the user named**, never a roster walk.

**Sequence, in the agent, starting from that list:**

1. The collector above already returned the app labels, so **the agent calls no roster tool
   here** — not `app_list`, not `server_list`. Safety rule 7 says a list response is built from
   the same `/server` payload that makes `server_get` a credential tool, and this is precisely
   the job that stated it would keep credentials out of the transcript; fetching a roster it was
   handed would give that away for nothing.
2. Filter: SSL expiring within the next 30 days → flag for renewal
3. For each flagged app: confirm whether Let's Encrypt auto-renewal is enabled. **There is no MCP read tool for auto-renewal status** — check it in the Cloudways Platform UI (Application → SSL Certificate) or via the direct API; `security_lets_encrypt_auto_renewal` is a W **toggle**, never call it just to inspect the setting. If auto-renewal is off — double flag and report it; the fix (enable auto-renewal / renew) is a write — hand it to `workflows-maintenance.md` §2 (`security_lets_encrypt_auto_renewal` / `security_lets_encrypt_renew`, both W with confirmation), don't execute it from this read-only playbook.

> **One certificate, on request, is a different job.** If the user names an app — "is
> shop.example.com's cert about to expire?" — `app_get` on that one app is the right call, and
> the one payload it returns is the cost of an answer that nothing else provides. That is not
> this section; this section is the weekly fleet review.

> If Let's Encrypt auto-renewal is active, Cloudways renews 30 days before expiry. If it fails to renew (DNS issue) — you'll get an alert. It's still worth reviewing manually once every two weeks.

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
2. For two or three servers: `monitoring_server_graph` in parallel, plus `app_list` per
   server for the application roster. Provider, region and size are already in the
   `server_list` rows from step 1 — `server_get` repeats them beside master credentials.
3. Compare: provider, region, size, RAM/CPU usage, applications

**Tip:** Cloudways sometimes groups one client's apps on the same server. This can be a problem in production: a spike in one application affects the others. In an audit for a new client, this is the first thing to check.
