---
name: freshbooks-curl
description: Query FreshBooks (invoices, clients, estimates, payments, expenses, projects, time tracking) from a shell with curl and a rotating OAuth token. Use when you want FreshBooks data without running the freshbooks-mcp server, in a script, or on a machine where the MCP isn't installed.
---

# FreshBooks from the shell

FreshBooks has a real REST API reachable server-side — no browser bridge, no signed-in
tab, no `fpx`. Authentication is **OAuth2 only**: there is no API key and no personal
access token, so a one-time browser authorize flow is unavoidable.

## The two things that break naive clients

**1. Refresh tokens are single-use and rotate.** Every refresh returns a *new* refresh
token and kills the one you used. If the replacement is not written to disk before the
process ends, the account is locked out and the only recovery is re-running the browser
flow. Never hand-roll the refresh — use `fb_access_token` from
`references/fb-token.sh`, which persists the rotation before returning, and never point
two tools at the same state file.

**2. Three identifiers that are not interchangeable.** `accountId` (alphanumeric, e.g.
`xZNQ1X`), `businessId` (integer), `businessUuid`. Each URL family takes a different one
and answers a mismatch with a bare **404** that reads like a missing record. Always
resolve first with `fb_ids`.

| Family | Path | Identifier |
| --- | --- | --- |
| Accounting | `/accounting/account/{accountId}/…` | `accountId` |
| Payments | `/payments/account/{accountId}/…` | `accountId` |
| Accounting (business) | `/accounting/businesses/{businessUuid}/…` | `businessUuid` |
| Projects | `/projects/business/{businessId}/…` | `businessId` |
| Time tracking | `/timetracking/business/{businessId}/…` | `businessId` |

## One-time setup

Register an app at <https://my.freshbooks.com/#/developer>. The redirect URI must be
**HTTPS with no query string** — `https://localhost` works and never needs to
resolve. Put `FRESHBOOKS_CLIENT_ID` and `FRESHBOOKS_CLIENT_SECRET` somewhere loadable
(e.g. `~/.secrets`).

Then run the authorize flow once:

```sh
set -a; . ~/.secrets; set +a

# 1. Print the authorize URL, open it, click Allow.
node references/fb-bootstrap.mjs url "$FRESHBOOKS_CLIENT_ID"

# 2. The browser fails to load https://localhost?code=… — that is expected.
#    Copy the whole URL from the address bar and exchange it (the code is single-use
#    and expires within minutes).
node references/fb-bootstrap.mjs exchange "$FRESHBOOKS_CLIENT_ID" "$FRESHBOOKS_CLIENT_SECRET" \
  https://localhost 'https://localhost?code=PASTE_HERE'
```

Save the printed `refresh_token` as `FRESHBOOKS_REFRESH_TOKEN`. It seeds the state file
on first use; after that the state file is the source of truth and the env value is
ignored until you re-bootstrap.

## Core call pattern

```sh
set -a; . ~/.secrets; set +a
. references/fb-token.sh

fb_ids                                    # resolve accountId / businessId / businessUuid
ACCT=$(fb_account_id)

fb_curl "/accounting/account/$ACCT/invoices/invoices?per_page=5" \
  | jq '.response.result.invoices[] | {id, invoice_number, amount, outstanding, status}'
```

`fb_curl <path> [curl args…]` attaches the bearer token and `Api-Version: alpha`;
everything after the path is passed to `curl`, so writes work too.

## Response envelopes differ per family

- Accounting / events → `.response.result.<name>`, errors at `.response.errors[].message`
- Accounting-business → `.data`, errors at `.errors.message` + `.errors.details[].reason`
- Projects / time tracking / comments → bare object, errors at `.error`
- Payments → errors at `.errors.details[].field`

A single `jq` path will not work across families — see `references/recipes.md`.

## Writes

Accounting writes wrap the payload in the **singular** resource name:

```sh
fb_curl "/accounting/account/$ACCT/invoices/invoices" \
  -X POST -H 'Content-Type: application/json' \
  -d '{"invoice":{"customerid":123,"create_date":"2026-08-12","lines":[]}}'
```

Money is `{"amount":"150.00","code":"USD"}` — the amount is a **string**, not a number.

Deletes on the accounting family are frequently soft deletes via `vis_state` on an
update rather than HTTP `DELETE`. Confirm per resource before assuming.

**A 200 is not proof a write persisted — re-read the record to confirm.**

## In context groups

When the freshbooks-mcp server is a member of an mcp-host registration, its tools carry
`_meta.mint` hints that place it in the **money** group. The one canonical read is
`freshbooks_list_invoices` for **what's due** ("what's owed?", "anything overdue?"): it
takes `view: "brief"` and answers one line per invoice,
`Invoice <number>, <client>, <amount> — <due date | no date> — <status>`, cut to 120 characters
as a whole. Client names are third-party text, so the lines arrive as `data` in the fleet's
untrusted-data envelope, with `-- ` note lines for an empty page (`-- none`) or a partial one
(`-- N of M shown`, `-- more`). It names no
subject — the account is fixed by the credential and clients are counterparties, not the
person's subjects — and no date range, since the list filters on raw FreshBooks params.
Everything else is a `lookup` read or a `change`/`send` write. A compound ask looks like
"what's due this week — and are any invoices overdue?", where the money group adds the
invoice lines to the other groups' answers. FreshBooks needs no browser, so it never
answers "needs your browser open"; a spent refresh token surfaces as a source that could
not answer until the authorize flow is re-run.

## Troubleshooting

| Symptom | Cause |
| --- | --- |
| `invalid_client` on refresh | The refresh grant needs `client_secret` **and** `redirect_uri`, form-encoded — not JSON |
| `invalid_grant` on refresh | The token was already spent. Re-run the bootstrap |
| 404 on a valid-looking record | Wrong identifier for that URL family — run `fb_ids` |
| 401 on every call | Access token stale and refresh failing; check the state file |

See `references/recipes.md` for ready-to-run request bodies and `jq` recipes.
