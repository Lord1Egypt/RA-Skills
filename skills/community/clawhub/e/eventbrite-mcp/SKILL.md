---
name: eventbrite
description: "Query eventbrite.com from a shell — your tickets/orders, your organizations' events and attendees via the documented token API (curl), and public event discovery/search via the fpx browser bridge (the search API is WAF-walled and absent from the documented API). Use when you want Eventbrite data without an MCP server, in a script, or one-shot."
---

# Eventbrite access (curl + fpx)

Two surfaces, two tools — match the tool to reachability:

1. **Documented API `https://www.eventbriteapi.com/v3`** — reachable
   server-side with a personal OAuth token. Use plain `curl`. Covers your
   identity, your orders/tickets, organizations you own (events, attendees,
   orders), and any event **by id**. It has **no public event search** —
   Eventbrite removed it from the documented API in 2019.
2. **Consumer site API `https://www.eventbrite.com/api/v3/destination/…`** —
   WAF-blocked for any server-side client (returns an HTML "Whoops!" page).
   Public event **search/discovery** lives only here, so those calls route
   through the user's signed-in browser tab with `fpx`.

## One-time setup

**Token (curl surface):** create a private token at
<https://www.eventbrite.com/platform/api-keys> (free for any Eventbrite
account) and export it as `EVENTBRITE_TOKEN`.

**Bridge (fpx surface):**

```sh
npm install -g @fetchproxy/cli                  # provides `fpx`
fpx profile add eventbrite --domain eventbrite.com
fpx pair -p eventbrite    # prints a pair code → approve in the ContextMint Bridge popup
```

Requires **ContextMint Bridge**
(<https://github.com/nullnet-app/contextmint-bridge/releases> — load the chrome
zip unpacked; use Chrome for now, Safari is not available yet) with site access for
`eventbrite.com` and an open (signed-in for account data) eventbrite.com tab.
Pairing persists after the first approval.
ContextMint Bridge is the fetchproxy extension renamed (same maintainer; source at <https://github.com/nullnet-app/contextmint-bridge> — build it, or verify a release zip with `shasum -a 256 -c contextmint-bridge-chrome-<version>.zip.sha256`).

## Core calls

Token surface — every request is:

```sh
curl -sS "https://www.eventbriteapi.com/v3/users/me/" \
  -H "Authorization: Bearer $EVENTBRITE_TOKEN" | jq
```

Bridge surface — stdout is data only, ready for `jq`:

```sh
fpx get 'https://www.eventbrite.com/api/v3/destination/events/?event_ids=<id>&expand=event_sales_status,primary_venue' \
  -p eventbrite | jq '.events[0]'
```

Ready-to-run request bodies and `jq` recipes: `references/token-api.md`
(curl surface) and `references/discovery-api.md` (fpx surface, incl. event
search). Read the relevant reference before composing a call — the search
body shape and the resolve-location-first rule live there.

## Rules

- **Resolve places before searching**: destination search takes place ids,
  not free-text locations — autocomplete first (see `discovery-api.md`).
- **Pagination**: v3 responses carry a `pagination` envelope; loop with
  `?continuation=<token>` while `has_more_items` is true.
- **fpx exit codes**: `2` bridge down (pair/approve in ContextMint Bridge), `3` bot
  wall (refresh a signed-in eventbrite.com tab), `4` upstream non-2xx.
- **Read-only**: these recipes only read data. The documented API supports
  organizer writes (create/update events etc.) but they are out of scope
  here — don't improvise write calls from this skill.
- Never log or commit the token or captured cookies.

## In context groups

When this server is hosted as the `eventbrite` MCP (mcp-host context groups),
every tool sits in the **family** group:

- **Canonical read:** `eb_my_orders` answers "what's on?" — the signed-in
  account's upcoming ticket orders. With `view: "brief"` it answers one line
  per order (`event name — start or "no date" — order status`) inside the
  untrusted-data envelope (an event name starting with `-- ` or `\` gets
  one leading `\`, so it never reads as a note), `-- none` when there is
  nothing, and
  `-- N of M shown` / `-- more` when the page is partial, followed by
  `-- next: continuation=<token>` — pass that token back as `continuation`
  for the next page. No subject (one
  token is one account) and no date range (Eventbrite filters orders by
  upcoming/past only).
- **Nothing answers what's-new or what's-due**; every other tool is a
  `lookup` (events, venues, organizers, organization reports, event search).
- **A compound ask** looks like "what tickets do we have coming up … and
  anything due at school?" — the family group answers the first half from
  `eb_my_orders`, the school group the second.
- **Browser:** the canonical read uses `EVENTBRITE_TOKEN` and never needs a
  browser. Only event discovery falls back to the browser bridge when no token
  is configured; there, the group answers "needs your browser open" when the
  signed-in eventbrite.com tab is not.
