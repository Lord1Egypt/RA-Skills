# FreshBooks curl recipes

All examples assume:

```sh
set -a; . ~/.secrets; set +a
. references/fb-token.sh
ACCT=$(fb_account_id)
BIZ=$(fb_ids | jq -r .businessId)
```

Paths marked **(unverified)** are transcribed from the official
`freshbooks-python-sdk` source but have not been exercised against a live account.

## Identity

```sh
fb_curl /auth/api/v1/users/me | jq '.response | {identity_id, email}'
fb_ids   # accountId / businessId / businessUuid — run before anything else
```

## Invoices

```sh
# List (newest first via FreshBooks' own sort param)
fb_curl "/accounting/account/$ACCT/invoices/invoices?per_page=25&page=1" \
  | jq '.response.result | {page, pages, total,
        invoices: [.invoices[] | {id, invoice_number, organization, create_date,
                                  amount: .amount.amount, outstanding: .outstanding.amount, status}]}'

# One invoice, with line items expanded
fb_curl "/accounting/account/$ACCT/invoices/invoices/INVOICE_ID?include[]=lines" \
  | jq '.response.result.invoice'

# Outstanding only — v3_status is the useful status field
fb_curl "/accounting/account/$ACCT/invoices/invoices?search[v3_status]=overdue" \
  | jq '[.response.result.invoices[] | {id, invoice_number, outstanding: .outstanding.amount}]'

# Total outstanding across a page
fb_curl "/accounting/account/$ACCT/invoices/invoices?per_page=100" \
  | jq '[.response.result.invoices[].outstanding.amount | tonumber] | add'
```

Create **(unverified)** — money amounts are strings:

```sh
fb_curl "/accounting/account/$ACCT/invoices/invoices" -X POST \
  -H 'Content-Type: application/json' -d '{
  "invoice": {
    "customerid": 123,
    "create_date": "2026-08-12",
    "lines": [
      { "name": "Consulting", "description": "August retainer",
        "qty": 1, "unit_cost": { "amount": "1500.00", "code": "USD" } }
    ]
  }
}' | jq '.response.result.invoice | {id, invoice_number, amount}'
```

## Clients

```sh
fb_curl "/accounting/account/$ACCT/users/clients?per_page=100" \
  | jq '[.response.result.clients[] | {id: .userid, organization, fname, lname, email}]'

# Find a client by name
fb_curl "/accounting/account/$ACCT/users/clients?search[organization_like]=acme" \
  | jq '.response.result.clients'
```

Create **(unverified)**:

```sh
fb_curl "/accounting/account/$ACCT/users/clients" -X POST \
  -H 'Content-Type: application/json' \
  -d '{"client":{"email":"ap@example.com","organization":"Example Co","fname":"Pat","lname":"Doe"}}' \
  | jq '.response.result.client | {userid, organization}'
```

## Payments

```sh
fb_curl "/accounting/account/$ACCT/payments/payments?per_page=50" \
  | jq '[.response.result.payments[] | {id, invoiceid, date, amount: .amount.amount, type}]'
```

Record a payment **(unverified)**:

```sh
fb_curl "/accounting/account/$ACCT/payments/payments" -X POST \
  -H 'Content-Type: application/json' \
  -d '{"payment":{"invoiceid":456,"amount":{"amount":"1500.00","code":"USD"},"date":"2026-08-12","type":"Check"}}'
```

## Estimates — accepting is an action, not a status write

`status`, `display_status` and `ui_status` are computed read-only fields and disagree with
each other (`status: 3` / `"viewed"` / `"open"` are the same estimate). Writing them does
nothing. Acceptance is an action on the estimate **(unverified — collection-derived)**:

```sh
fb_curl "/accounting/account/$ACCT/estimates/estimates/279405" -X PUT \
  -H 'Content-Type: application/json' \
  -d '{"estimate":{"action_accept":true}}' \
  | jq '.response.result.estimate | {id, accepted, status, display_status, ui_status}'
```

Email it to the client — note `estimate_customized_email`, not the invoice endpoint's
`invoice_customized_email`:

```sh
fb_curl "/accounting/account/$ACCT/estimates/estimates/279405" -X PUT \
  -H 'Content-Type: application/json' \
  -d '{"estimate":{"action_email":true,"email_recipients":["client@example.com"]}}'
```

There is **no decline**: no declined status, no `action_deny`, no `estimate.decline`
webhook. The nearest expressible thing is the soft delete, `{"estimate":{"vis_state":1}}`,
which removes it rather than declining it.

## Full accounting resource map

Same family and envelope; only the path suffix and list key change. Four of these are not
what you would guess — they are marked ⚠ and each cost a 404 before the SDK settled it.

| Resource | Path suffix | List key |
| --- | --- | --- |
| Invoices | `invoices/invoices` | `invoices` |
| Clients | `users/clients` | `clients` |
| Estimates | `estimates/estimates` | `estimates` |
| Payments | `payments/payments` | `payments` |
| Credit notes | `credit_notes/credit_notes` | `credit_notes` |
| Invoice profiles | `invoice_profiles/invoice_profiles` | `invoice_profiles` |
| Items | `items/items` | `items` |
| Taxes | `taxes/taxes` | `taxes` |
| Expenses | `expenses/expenses` | `expenses` |
| Expense categories ⚠ | `expenses/categories` | `categories` |
| Staff ⚠ | `users/staffs` | `staff` |
| Gateways ⚠ | `systems/gateways` | `gateways` |
| Other income ⚠ | `other_incomes/other_incomes` | `other_income` |
| Tasks (billable catalogue) | `projects/tasks` | `tasks` |
| Bills | `bills/bills` | `bills` |
| Bill vendors | `bill_vendors/bill_vendors` | `bill_vendors` |
| Bill payments | `bill_payments/bill_payments` | `bill_payments` |

`projects/tasks` is in the **accounting** family (accountId) despite the prefix.

### `total` can exceed the rows you get back

Verified live: expenses returned `total: 16` with an empty array — the count includes
records the identity cannot read, and paging never surfaces them. Always check both:

```sh
fb_curl "/accounting/account/$ACCT/expenses/expenses?per_page=100" \
  | jq '{total: .response.result.total, rows: (.response.result.expenses|length)}'
```

If `rows` is 0 while `total` is not **and you are on a page within range**, that is a
permission boundary rather than an empty account. Check the page first — an empty page with
a non-zero total is also just what paging past the end looks like:

```sh
fb_curl "/accounting/account/$ACCT/expenses/expenses?per_page=100" \
  | jq '.response.result | {total, pages, page, rows: (.expenses|length),
         verdict: (if (.expenses|length) > 0 then "ok"
                   elif .page > .pages then "past the last page"
                   else "rows withheld by permissions" end)}'
```

```sh
fb_curl "/accounting/account/$ACCT/expenses/expenses?per_page=50" \
  | jq '[.response.result.expenses[] | {id, date, amount: .amount.amount, vendor, notes}]'
```

## Projects and time tracking — different id, different envelope

These take `businessId` and return **bare** objects, not `.response.result`. Pagination
lives under `meta`, so `.response.result.total` reads `undefined` here and looks like an
empty account:

```sh
fb_curl "/projects/business/$BIZ/projects" \
  | jq '{meta, projects: [.projects[] | {id, title, client_id, active}]}'

# time_entries' meta also carries total_logged and total_unbilled
fb_curl "/timetracking/business/$BIZ/time_entries" \
  | jq '{logged: .meta.total_logged, unbilled: .meta.total_unbilled,
         entries: [.time_entries[] | {id, project_id, duration, started_at, note}]}'

fb_curl "/comments/business/$BIZ/services" | jq '[.services[] | {id, name, billable}]'
```

Errors here are `.error`, a plain string — not `.response.errors[]`.

These endpoints work on a business with **no accounting account**, so they can succeed
when every `/accounting/account/...` call fails.

Log time (duration is in **seconds**):

```sh
fb_curl "/timetracking/business/$BIZ/time_entries" -X POST \
  -H 'Content-Type: application/json' \
  -d '{"time_entry":{"duration":3600,"started_at":"2026-08-12T09:00:00Z","note":"Design review"}}'
```

## Pagination

Accounting lists carry `page`, `pages`, `per_page`, `total` on the result envelope.
Walk them:

```sh
p=1
while :; do
  body=$(fb_curl "/accounting/account/$ACCT/invoices/invoices?per_page=100&page=$p")
  printf '%s' "$body" | jq -c '.response.result.invoices[]'
  pages=$(printf '%s' "$body" | jq -r '.response.result.pages')
  [ "$p" -ge "$pages" ] && break
  p=$((p + 1))
done
```

## Error shapes by family

```sh
# Accounting / events
jq -r '.response.errors[]? | "\(.errno): \(.message)"'
# Accounting-business
jq -r '.errors? | "\(.message) \(.details[]?.reason // "")"'
# Payments
jq -r '.errors?.details[]? | "\(.field): \(.message)"'
# Projects / time tracking / comments / uploads
jq -r '.error? // empty'
```
