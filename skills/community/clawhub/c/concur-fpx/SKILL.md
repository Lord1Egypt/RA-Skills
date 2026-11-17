---
name: concur-fpx
description: "Read SAP Concur expense data from a shell — your expense reports, each report's line items (vendor, type, amounts, receipts, exceptions), and available expenses not yet on a report — through the user's signed-in Concur browser tab with the fpx CLI. Use when asked about Concur expenses, expense reports, reimbursement/payment status, what's unsubmitted, or unassigned card/receipt expenses."
---

# SAP Concur access (fpx)

Concur's web app talks to a GraphQL API at
`https://www-<dc>.api.concursolutions.com/spend-graphql/graphql`, authed only by
the browser's session cookies (`credentials: include`, no bearer header) and
fronted by Akamai bot management. So every call routes through the user's
signed-in Concur tab with `fpx`, relayed by the `<dc>.concursolutions.com` tab
(`--via-tab`) because the API host serves no page of its own.

Read-only. Introspection is disabled; every query in `queries/` was verified live.

## One-time setup

```sh
npm install -g @fetchproxy/cli          # provides `fpx`
fpx profile add concur --domain concursolutions.com
fpx pair -p concur                      # approve the pair code in ContextMint Bridge
```

Needs **ContextMint Bridge** in Chrome and an open, signed-in Concur tab
(`https://us2.concursolutions.com/…`). Approve the pair code **in the browser that
holds the Concur session** — if ContextMint Bridge runs in more than one browser,
each one dials the same port and a code approved in the wrong one pins that
browser. Fix: `fpx trust clear fpx-concur`, then pair again in the right one.
Lines like `refusing an extension whose identity is not the one this MCP paired
with` on stderr are the *other* browser being turned away; the call still works.

Datacenter: `CONCUR_DC` (default `us2`) — read it off the signed-in tab's host
(`us2.concursolutions.com` → `us2`; `eu2`, …). Sessions are short: when calls
start failing with exit 4 / HTTP 401, reload or sign back in to the tab.

## Core call

`scripts/concur-gql <query> [vars-json]` — `<query>` is a file under `queries/`
by name (or any `.graphql` path). stdout is the GraphQL JSON, ready for `jq`.

```sh
G=~/.claude/skills/concur-fpx/scripts/concur-gql
$G reports '{"status":"ALL"}' | jq '.data.employee.reportsForUser.list'
```

| Query | Vars | Returns |
|---|---|---|
| `whoami` | — | `userId` (UUID) + role |
| `reports` | `status` (`ALL`/`ACTIVE`/`UNSUBMITTED`/`SENT_FOR_PAYMENT`), `range` `{start,end}` `YYYY-MM-DD`, `page`, `size` | report list + pagination |
| `report` | `userId` (**required, from `whoami`**), `reportId` | report header + every entry |
| `available-expenses` | `page`, `size` | expenses not yet on a report |

**Resolve-first rule:** `employee(userId: "")` resolves to the signed-in user, so
most queries need no id — but `reportEntriesDetails` (inside `report`) rejects
`""` with a 400. Run `whoami` first and pass the real `userId` to `report`.

GraphQL errors arrive on HTTP 200 as `.errors[]` with the opaque message
`"An error occurred"` — check `.errors` before trusting `.data`; the
`extensions.dataSource` / `response.status` fields say which backend refused.

Exit codes (from fpx): `2` bridge down / pairing pending · `3` bot wall ·
`4` upstream non-2xx (401 = signed out).

Ready-to-run `jq` recipes: `references/recipes.md`. The full operation list the
web app uses (≈130 queries, ≈50 mutations — writes deliberately not wired) is in
`references/operations.md`, for extending this.
