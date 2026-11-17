---
name: crowntown-portal
description: >-
  Access the Crown Town Compost customer portal (portal.crowntowncompost.com) —
  pickup/service history, invoices, upcoming service days, skips, account
  details — from a shell with curl instead of running the crowntowncompost-mcp
  server. Logs in with a Django username/password form POST to get a session
  cookie, then curls two JSON endpoints and a few server-rendered pages. Use
  when you want Crown Town Compost data without the MCP, in a script, or on a
  machine where the MCP isn't installed.
---

# Crown Town Compost portal via curl (no MCP)

`crowntowncompost.com` is only a marketing site. All customer data lives at
**`portal.crowntowncompost.com`** — a **Django** app (a white-labeled
**StopSuite** hauler platform; it CNAMEs to `crowntown.stopsuite.com`).

It is reachable **server-side**: no bot wall, no browser bridge, no `fpx`, no
Transporter extension. Auth is a real **username + password form POST** that
returns an HttpOnly `sessionid` cookie. `curl` with a cookie jar reaches
everything a signed-in customer can see.

Two of the richest surfaces are clean **JSON** endpoints (service history and
billing); the rest are server-rendered HTML.

## The one thing that trips people up: Django CSRF

Every **POST** (including the login and the two JSON reads) needs all of:

- the `csrftoken` cookie (set by any GET), sent back in the cookie jar
- an `X-CSRFToken:` header **equal to that cookie's value**
- `Origin:` and `Referer:` headers on the portal's own origin — Django rejects
  HTTPS POSTs that lack them, with a 403, *before* looking at your credentials

GETs need none of this. A 403 on a POST almost always means a missing header,
not a bad password.

## One-time setup

```sh
export CROWNTOWN_USERNAME='you@example.com'
export CROWNTOWN_PASSWORD='your-portal-password'   # or: op read "op://Private/CrownTown/password"
export CT=https://portal.crowntowncompost.com
JAR=~/.cache/crowntown-cookies.txt
mkdir -p ~/.cache && : > "$JAR"
```

## Log in (get the session cookie)

Read the password from stdin (`password@-`) rather than putting it in argv —
`--data-urlencode name=value` exposes the value to any local user via `ps`
while the process runs.

```sh
# 1. GET the login page to pick up the csrftoken cookie + the hidden form token.
CSRF_FORM=$(curl -s -c "$JAR" -b "$JAR" "$CT/accounts/login/?next=/accounts/" \
  | grep -o 'name="csrfmiddlewaretoken" value="[^"]*"' | head -1 | sed 's/.*value="//;s/"$//')
CSRF_COOKIE=$(awk '$6=="csrftoken"{print $7}' "$JAR" | tail -1)

# 2. POST the credentials. Do NOT follow redirects (-L) here: the 302's
#    Set-Cookie carries the sessionid, and success is "302 away from login".
printf '%s' "$CROWNTOWN_PASSWORD" | curl -s -c "$JAR" -b "$JAR" \
  -H "X-CSRFToken: $CSRF_COOKIE" -H "Origin: $CT" \
  -H "Referer: $CT/accounts/login/?next=/accounts/" \
  --data-urlencode "csrfmiddlewaretoken=$CSRF_FORM" \
  --data-urlencode "username=$CROWNTOWN_USERNAME" \
  --data-urlencode "password@-" \
  --data-urlencode "next=/accounts/" \
  -o /dev/null -D - "$CT/accounts/login/?next=/accounts/" \
  | grep -iE '^(HTTP/|location:)'
```

**Success** = `HTTP/2 302` + a `location:` that is NOT `/accounts/login/`, and
a `sessionid` now in the jar. A `200` means the login page re-rendered — wrong
username/password. Confirm the jar:

```sh
grep -q sessionid "$JAR" && echo "signed in" || echo "NOT signed in"
```

The `csrftoken` cookie **rotates on login** — always re-read it from the jar
before each POST:

```sh
csrf() { awk '$6=="csrftoken"{print $7}' "$JAR" | tail -1; }
```

## The two JSON endpoints (the good stuff)

Both are **POST**, form-urlencoded, and return `{meta, qs, data[]}`. They use
the **Metronic KTDatatable** grammar — `pagination[page]`, `pagination[perpage]`,
`sort[field]`, `sort[sort]`, `query[<field>]` — *not* DataTables' `draw/start/length`.

```sh
ctpost() {  # ctpost <path> [extra --data-urlencode args...]
  local path="$1"; shift
  curl -s -b "$JAR" -c "$JAR" \
    -H "X-CSRFToken: $(csrf)" -H 'X-Requested-With: XMLHttpRequest' \
    -H "Origin: $CT" -H "Referer: $CT$path" \
    "$@" "$CT$path"
}
```

### Service history (pickups)

```sh
ctpost /accounts/stops/api/ \
  --data-urlencode 'pagination[page]=1' \
  --data-urlencode 'pagination[perpage]=20' \
  --data-urlencode 'sort[field]=date' --data-urlencode 'sort[sort]=desc' \
| jq '{total: .meta.total, pages: .meta.pages,
       stops: [.data[] | {date, status, time: .timestamp, weight, services}]}'
```

Filter by outcome — **the values are lowercase**; a capitalized `Missing`
silently returns zero rows:

```sh
ctpost /accounts/stops/api/ --data-urlencode 'query[status]=missing' \
  --data-urlencode 'pagination[perpage]=50' | jq '.meta.total, [.data[].date]'
```

Valid: `success | missing | empty | inaccessible | unacceptable` (omit for all).

### Billing history (invoices)

```sh
ctpost /accounts/billing-history/api/ \
  --data-urlencode 'pagination[perpage]=20' \
  --data-urlencode 'sort[field]=date' --data-urlencode 'sort[sort]=desc' \
| jq '[.data[] | {number, date, amount, status, is_payable, pay: .hosted_invoice_url}]'
```

Open invoices are `is_payable: true`; `hosted_invoice_url` / `invoice_pdf` /
`receipt_url` are Stripe links. **Pay in a browser** — don't script payments.

## Server-rendered pages (GET, parse the HTML)

| What | Path |
|---|---|
| Dashboard (subscription, next service, addresses) | `/accounts/` |
| Environmental impact numbers (htmx fragment) | `/accounts/impact-statistics/` |
| Account details form (name, phone, notification prefs) | `/accounts/update/` |
| Service calendar (upcoming + skip buttons) | `/accounts/service-calendar/` |
| Service history page (shell around the JSON above) | `/accounts/service-history/` |
| Support form | `/accounts/support/` |

```sh
ctget() { curl -s -b "$JAR" -c "$JAR" "$CT$1"; }
```

Impact numbers are the easiest scrape (plain text in a small fragment):

```sh
ctget /accounts/impact-statistics/ \
  | grep -oE '[0-9.,]+ (lbs diverted|seedlings planted|miles offset|gallons of gas)'
```

Upcoming skippable service days — each `.submit-skip` button carries the ids a
skip needs:

```sh
ctget /accounts/service-calendar/ \
  | grep -o '<button[^>]*submit-skip[^>]*>' \
  | sed -E 's/.*data-action="([^"]*)".*data-clid="([^"]*)".*data-rid="([^"]*)".*data-route-date="([^"]*)".*/\4  rid=\3 clid=\2 action=\1/'
```

`action="skip"` = currently scheduled (skipping it will skip it);
`action="unskip"` = already skipped.

## In context groups

When the crowntowncompost-mcp server is hosted on mcp-host, its tools carry
`_meta.mint` hints that put it in the **home** group, so a person can ask the
whole group at once instead of naming this service.

- **What's on** — `crowntown_list_upcoming_services` (canonical). With
  `view: "brief"` it answers one line per collection day:
  `Compost pickup — 2026-08-07 — scheduled` (or `skipped`), and `-- none`
  when nothing is upcoming.
- **What's due** — `crowntown_list_invoices` (canonical). With
  `view: "brief"` it lists the payable invoices only (unless
  `payable_only: false`), one line each, `Invoice <number> <amount> —
  <ISO date> — <status>`, inside the untrusted-data envelope (`data: [...]`);
  `-- none` when nothing is owed, `-- N of M shown` when the page is partial.
- **No subjects.** The server signs in to one portal account and no tool
  takes an address or account to choose between, so neither read takes a
  subject; neither takes a date range either.
- No "what's new" read: service history, the dashboard, the pickup schedule
  and the account are lookups; skipping a day and updating the account are
  changes; reporting a missed pickup and contacting support are sends.

A compound ask looks like "when's compost pickup, and do I owe anything for
it?" — the group's whats-on and whats-due reads answer the two halves. This
server signs in with a username and password from the server side, so it needs
no open browser.

## Writes (all POST; see `references/endpoints.md` for full field lists)

**A 302 is not proof a write persisted — always re-read to verify.**

```sh
# Skip an upcoming service (rid/clid/action from the calendar above)
ctpost /accounts/service-calendar/skip-service/ \
  --data-urlencode 'rid=2815' --data-urlencode 'clid=3360' \
  --data-urlencode 'action=skip' >/dev/null
# verify: the same day's button should now read action="unskip"
```

Other write endpoints (each POSTs to its own URL, with `csrfmiddlewaretoken`):
`/accounts/report-missed-pickup/` (`date`, `comment`),
`/accounts/update/` (`first_name`, `last_name`, `phone`, `send_email_reminders`,
`service_notifications` — **read-modify-write**: re-send every field, since
omitted checkboxes mean "off"), `/accounts/support/` (`message`, `email`, `phone`),
`/accounts/cancellation-request/` (per-location dynamic field names — read the
GET form first).

## Session expiry

An authed request that returns the login page (or redirects to
`/accounts/login/`) means the session expired — re-run the login block. Detect it:

```sh
ctget /accounts/ | grep -q 'm_login_signin_submit' && echo "session expired"
```

## Troubleshooting

| Symptom | Cause |
|---|---|
| `403` on any POST | Missing `X-CSRFToken` / `Origin` / `Referer`, or a stale `csrftoken` (re-read it from the jar after login) |
| Login returns `200` | Wrong username/password (the page just re-rendered) |
| JSON endpoint returns HTML | Session expired — log in again |
| `query[status]` returns 0 rows | You capitalized the value; use lowercase |
| Empty `data[]` with a large `perpage` | You're past the last page — check `meta.pages` |
