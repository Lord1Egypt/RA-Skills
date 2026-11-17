# Crown Town Compost portal — endpoint reference

Ready-to-run request bodies for `portal.crowntowncompost.com` (Django /
StopSuite). Assumes the `$CT`, `$JAR`, `csrf()`, `ctget()`, `ctpost()` helpers
from `SKILL.md` are already defined and you are signed in.

All shapes were live-verified 2026-07-31 against a signed-in customer account.

---

## Response envelope (both JSON endpoints)

```json
{
  "meta": { "page": 1, "pages": 4, "perpage": 20, "total": 61,
            "sort": "desc", "field": "date", "rowIds": [157404] },
  "qs": "<serialized query state>",
  "data": [ /* rows */ ]
}
```

Request grammar (Metronic KTDatatable):

| Param | Meaning |
|---|---|
| `pagination[page]` | 1-based page number |
| `pagination[perpage]` | rows per page (20 default) |
| `sort[field]` | column field name |
| `sort[sort]` | `asc` \| `desc` |
| `query[<field>]` | per-column filter |
| `query[generalSearch]` | free-text search |

---

## POST `/accounts/stops/api/` — service history

Sortable/filterable fields: `RecordID, address, date, status, timestamp, services`.

Row:

```json
{ "RecordID": 157404, "status": "Success", "timestamp": "9:34 a.m.",
  "address": "123 Example Street", "weight": "35", "nickname": "",
  "date": "Friday, Jul 31, 2026", "services": "35 x1" }
```

- `status` displays capitalized (`Success`/`Missing`/`Empty`/`Inaccessible`/`Unacceptable`)
  but **`query[status]` matches lowercase only**.
- `services` is `<service code> x<count>` — `x0` on a missed stop.
- `weight` is in lbs and is empty when nothing was collected.

Recipes:

```sh
# Every missed pickup, newest first
ctpost /accounts/stops/api/ \
  --data-urlencode 'query[status]=missing' \
  --data-urlencode 'pagination[perpage]=100' \
  --data-urlencode 'sort[field]=date' --data-urlencode 'sort[sort]=desc' \
| jq -r '.data[] | "\(.date)  \(.status)"'

# Total weight diverted across all recorded stops
ctpost /accounts/stops/api/ --data-urlencode 'pagination[perpage]=100' \
| jq '[.data[].weight | select(. != "") | tonumber] | add'

# Success rate
ctpost /accounts/stops/api/ --data-urlencode 'pagination[perpage]=100' \
| jq '[.data[].status] | {total: length, success: map(select(.=="Success")) | length}'

# Page through everything
for p in $(seq 1 4); do
  ctpost /accounts/stops/api/ --data-urlencode "pagination[page]=$p" \
    --data-urlencode 'pagination[perpage]=20' | jq -c '.data[] | {date,status}'
done
```

---

## POST `/accounts/billing-history/api/` — invoices

Row:

```json
{ "RecordID": 1, "number": "INV-1", "date": "Jul 1, 2026", "amount": "$44.00",
  "status": "paid", "invoice_pdf": "https://…", "receipt_url": "https://…",
  "hosted_invoice_url": "https://…", "is_payable": false, "invoice_id": 11 }
```

Stripe-backed. `is_payable: true` marks an open invoice.

```sh
# Open invoices with their payment links
ctpost /accounts/billing-history/api/ --data-urlencode 'pagination[perpage]=50' \
| jq -r '.data[] | select(.is_payable) | "\(.date)  \(.amount)  \(.hosted_invoice_url)"'

# Total billed over the returned window
ctpost /accounts/billing-history/api/ --data-urlencode 'pagination[perpage]=100' \
| jq '[.data[].amount | gsub("[$,]";"") | tonumber] | add'
```

CSV export (returns a file):

```sh
ctpost /accounts/billing-history/csv/ \
  --data-urlencode "csrfmiddlewaretoken=$(csrf)" \
  --data-urlencode 'qs=' -o billing.csv
```

---

## GET pages worth scraping

### `/accounts/` — dashboard

Server-rendered. Useful anchors:

- `.account-status-item` × 3 → `Account Status`, `Active Subscriptions`, `Next Service`
- `.m-badge--wide` → subscription status (`Active`)
- `$44.00/month` → price + period
- `Renews …` → **rendered twice** (a short `August 1` then the full
  `August 1, 2026, 1:00 a.m.`). Match the form that carries a year, or you get the short one.
- The Service Address card's `<table>` → address + service day(s)

```sh
ctget /accounts/ | grep -o 'account-status-item[^<]*<[^>]*>[^<]*' | head
ctget /accounts/ | grep -oE '\$[0-9,]+\.[0-9]{2}/[a-z]+'
```

### `/accounts/impact-statistics/` — htmx fragment

```sh
ctget /accounts/impact-statistics/ \
  | grep -oE '[0-9.,]+ (lbs diverted|seedlings planted|miles offset|gallons of gas)'
```

### `/accounts/update/` — account details form

Current values live in the `value=""` attributes; the two preference toggles are
checkboxes (`checked` present = on).

```sh
ctget /accounts/update/ \
  | grep -oE 'name="(first_name|last_name|phone)" value="[^"]*"'
ctget /accounts/update/ | grep -oE '<input[^>]*name="(send_email_reminders|service_notifications)"[^>]*>'
```

### `/accounts/service-calendar/` — upcoming days + skip ids

Each skippable day renders:

```html
<button class="btn m-btn btn-sm submit-skip" data-action="skip" data-clid="3360"
        data-rid="2815" data-route-date="Aug. 7, 2026" data-skip-has-credit="false">Skip Service</button>
```

Non-skippable days render a plain `Not Skippable` label instead.

---

## Writes

Every POST carries `csrfmiddlewaretoken` plus the headers from `SKILL.md`.
**Re-read after every write — a 302 only means the request was accepted.**

### Skip / un-skip a service — `/accounts/service-calendar/skip-service/`

```sh
ctpost /accounts/service-calendar/skip-service/ \
  --data-urlencode "csrfmiddlewaretoken=$(csrf)" \
  --data-urlencode 'rid=2815' --data-urlencode 'clid=3360' \
  --data-urlencode 'action=skip'

# verify — the button for that rid/clid should now say action="unskip"
ctget /accounts/service-calendar/ | grep -o 'data-action="[^"]*" data-clid="3360" data-rid="2815"'
```

### Report a missed pickup — `/accounts/report-missed-pickup/`

`date` is bound to a datepicker with format `yyyy-mm-dd` — send ISO. Success is a
**302**; a **200** is Django re-rendering the form with errors (look for
`ul.errorlist`), meaning nothing was submitted.

```sh
ctpost /accounts/report-missed-pickup/ \
  --data-urlencode "csrfmiddlewaretoken=$(csrf)" \
  --data-urlencode 'date=2026-07-24' \
  --data-urlencode 'comment=Bin was out by 6am, not collected.'
```

### Update account details — `/accounts/update/` (read-modify-write)

Send **every** field: omitted checkboxes are read as "off", so a partial POST
silently turns preferences off. Checked boxes submit `on`.

```sh
ctpost /accounts/update/ \
  --data-urlencode "csrfmiddlewaretoken=$(csrf)" \
  --data-urlencode 'first_name=Test' --data-urlencode 'last_name=User' \
  --data-urlencode 'phone=555-555-5555' \
  --data-urlencode 'service_notifications=on'      # send_email_reminders omitted ⇒ off

# verify
ctget /accounts/update/ | grep -oE 'name="phone" value="[^"]*"'
```

### Contact support — `/accounts/support/`

The form pre-fills `email` and `phone` from the account; send them (a browser
does). As above, a 302 means accepted and a 200 re-render means rejected.

```sh
ctpost /accounts/support/ \
  --data-urlencode "csrfmiddlewaretoken=$(csrf)" \
  --data-urlencode 'message=Please confirm my next pickup date.' \
  --data-urlencode 'email=you@example.com'
```

### Request cancellation — `/accounts/cancellation-request/`

Field names are **per-location dynamic** (`cancel_location_<locId>`,
`final_route_<locId>`, `cf_<n>`), so read the GET form first and echo its fields
back:

```sh
ctget /accounts/cancellation-request/ | grep -oE '<(input|select)[^>]*name="[^"]*"'
```

Not scripted here on purpose — cancelling service is a consequential write; do
it deliberately.

---

## Out of scope

`/accounts/shop/`, `/accounts/checkout/`, `/gift-certificates/` involve payment.
Open them in a browser; don't script card entry.
