# Concur recipes (all live-verified 2026-10-08)

```sh
G=~/.claude/skills/concur-fpx/scripts/concur-gql
```

## Who am I

```sh
uid=$($G whoami | jq -r .data.employee.userId)
```

## Reports — table

```sh
$G reports '{"status":"ALL","range":{"start":"2025-01-01","end":"2026-12-31"}}' |
  jq -r '.data.employee.reportsForUser.list[] |
    [.reportDate, .reportNumber, .name, .approvalStatus, .paymentStatus,
     "\(.reportTotal.value) \(.reportTotal.currencyCode)"] | @tsv'
```

Unsubmitted only: `'{"status":"UNSUBMITTED"}'`. Paid/sent for payment:
`'{"status":"SENT_FOR_PAYMENT"}'`. Statuses come back as display strings
(`"Not Submitted"`, `"Not Paid"`, …). `approver` is null until submitted.

## One report with its line items

```sh
uid=$($G whoami | jq -r .data.employee.userId)
rid=$($G reports '{"status":"ALL"}' | jq -r '.data.employee.reportsForUser.list[0].reportId')
$G report "$(jq -nc --arg u "$uid" --arg r "$rid" '{userId:$u,reportId:$r}')" |
  jq -r '.data.reportEntriesDetails.entries[].summary |
    [.transactionDate, (.vendor.name // .vendor.description), .expenseType.name,
     "\(.transactionAmount.value) \(.transactionAmount.currencyCode)",
     "\(.postedAmount.value) \(.postedAmount.currencyCode)",
     (if .meta.hasReceiptImage then "receipt" else "NO RECEIPT" end)] | @tsv'
```

`transactionAmount` is in the spend currency; `postedAmount` is converted to the
report currency. The vendor usually lands in `vendor.description`, not `name`.

## Available (unassigned) expenses

```sh
$G available-expenses |
  jq -r '.data.employee.availableExpensesWithPagination.availableExpenses[] |
    [(.transactionDate // "?"), (.vendor // "?"), .expenseType.name,
     "\(.transactionAmount.value) \(.transactionAmount.currencyCode // "")",
     (.meta.missingData | join(","))] | @tsv'
```

A row with every field null and `missingData` set is a receipt still being
read (or one that never parsed) — not an error.

## Not covered (yet)

- **Trips / itineraries** — the travel side is the classic ASP portal
  (`/travelportal/triplibrary.asp`), not this GraphQL API.
- **Receipt images** — `receiptImageId` is exposed but the image fetch is not
  wired (would need `fpx profile declare concur --allow-download`, which forces
  a re-pair).
- **Writes** (create/submit/recall reports, move expenses) — exist as mutations
  in `operations.md`, deliberately not exposed.
