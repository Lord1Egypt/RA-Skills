---
name: checkly-usage
description: Inspect Checkly account plans, entitlements, feature limits, organization contract usage, credits, projections, and per-period consumption with npx checkly account plan and account usage. Use when reviewing plan availability, private-location or feature entitlements, usage terms, credit budgets, projected exhaustion, usage by account or check type, date ranges, or paginated usage data. Triggers on checkly account plan, checkly account usage, plan limits, entitlements, usage terms, usage summary, usage series, Checkly credits, contract usage, credit projection.
---

# Checkly account plan and usage

Use the read-only `npx checkly account` commands for two different questions:

- `account plan` reports the active account's plan, add-ons, entitlements, and feature limits. Use it for questions such as whether private locations or another feature is enabled.
- `account usage` reports organization contract terms, credit consumption, projections, and grouped usage series. It requires an account covered by usage terms; do not substitute it for plan or entitlement checks.

## Preconditions

```bash
npx checkly whoami
```

Confirm the active account before interpreting either account-level result. `whoami` prints the account, user, plan, and add-ons, but not the user's role. Usage reporting requires a current user or service API key and an Owner or Admin role; legacy account API keys are not accepted. If authentication is unclear, follow `checkly-auth` without printing credential values.

## Command map

| Command | Purpose | Exact output formats |
|---|---|---|
| `npx checkly account plan` | Show the plan and feature entitlements, or inspect one entitlement key | <code>[-o table&#124;json&#124;md]</code> (`table` default) |
| `npx checkly account usage terms` | Show contract dates, usage start date, credit budget/rates, and covered accounts | <code>[-o detail&#124;json&#124;md]</code> (`detail` default) |
| `npx checkly account usage summary` | Show totals for a date range and credit projections as of today | <code>[-o detail&#124;json&#124;md]</code> (`detail` default) |
| `npx checkly account usage series` | Show per-period usage grouped by account and/or check type | <code>[-o table&#124;json&#124;md]</code> (`table` default) |

`terms` and `summary` do not accept `table`; `series` does not accept `detail`.

## Account plan and entitlements

```bash
# Plan, add-ons, location availability, and all entitlements
npx checkly account plan --output json

# Search entitlement names and descriptions
npx checkly account plan --search "browser" --output json

# Inspect one entitlement by its exact key
npx checkly account plan <ENTITLEMENT_KEY> --output json

# Show features not included in the active plan
npx checkly account plan --disabled --output table
```

- `--type` accepts `metered` or `flag`.
- A positional entitlement `KEY` cannot be combined with `--type`, `--search`, or `--disabled`.
- Unfiltered JSON is a plan object with `plan`, `planDisplayName`, `addons`, optional `locations`, and `entitlements[]`. Inspect `locations.all[].available` and `locations.maxPerCheck` for public-location availability and per-check limits.
- Filtered JSON is an entitlement array; a `KEY` lookup returns one entitlement object. Filters do not include the surrounding plan or location fields.
- Use plan output for feature availability and limits. Use usage output only for contract-credit accounting.

## Usage date resolution

`--to` defaults to today, selects the usage terms covering that date, and is the inclusive end date for `terms`, `summary`, and `series`. For `summary` and `series`, `--from` defaults to the selected terms' `usageStartDate`.

Pin both dates explicitly whenever you paginate, compare `summary` with `series`, or collect results across commands or sessions. The usage API binds a series cursor to every resolved query parameter; relying on a moving default date can invalidate the next page.

## Recommended usage review workflow

First resolve one contract and choose the intended range. Unless a narrower range is required, copy `terms.usageStartDate` into `FROM` and use the same explicit `TO` for all commands.

```bash
TO=2026-03-31
FROM=2026-01-01

# 1. Resolve the contract that covers TO
npx checkly account usage terms \
  --to "$TO" \
  --output json

# 2. Review totals and projections for the pinned range
npx checkly account usage summary \
  --from "$FROM" \
  --to "$TO" \
  --output json

# 3. Break consumption down using the same range
npx checkly account usage series \
  --from "$FROM" \
  --to "$TO" \
  --interval month \
  --group-by account,checkType \
  --limit 100 \
  --output json
```

Report the contract period and credit budget before consumption percentages or projections. Distinguish measured usage from projections, which are calculated as of today.

## JSON response shapes

The JSON views are not interchangeable. Abbreviated shapes:

```jsonc
// account usage terms --output json
{
  "id": "usage-terms-id",
  "name": "Organization name",
  "accounts": [{ "id": "account-id", "name": "Account name" }],
  "contractStartDate": "YYYY-MM-DD",
  "contractEndDate": "YYYY-MM-DD",
  "usageStartDate": "YYYY-MM-DD",
  "creditBudget": 100000,
  "standardCreditsPerUnit": 1,
  "premiumCreditsPerUnit": 2
}

// account usage summary --output json
{
  "usageTermsId": "usage-terms-id",
  "period": { "from": "YYYY-MM-DD", "to": "YYYY-MM-DD" },
  "totals": {
    "credits": { "used": 123, "percentOfBudget": 12.3 },
    "meters": [
      { "meterType": "CHECK_RUN", "measures": { "...": "..." } },
      { "meterType": "AI_INVOCATION", "measures": { "...": "..." } }
    ]
  },
  "projections": {
    "weeksSinceStart": 4,
    "weeksRemaining": 48,
    "remainingCredits": 99877,
    "windows": {
      "sinceStart": {
        "usage": { "credits": {}, "meters": [] },
        "projectedAnnualPercentOfBudget": 10,
        "projectedCreditsAtContractEnd": 10000,
        "projectedPercentAtContractEnd": 10,
        "projectedWeeksUntilExhausted": null
      },
      "last30Days": {},
      "last7Days": {},
      "last1Day": {}
    }
  }
}

// account usage series --output json
{
  "data": [{
    "periodStart": "YYYY-MM-DD",
    "periodEnd": "YYYY-MM-DD",
    "accountId": "account-id",
    "checkType": "API",
    "credits": { "used": 12, "percentOfBudget": 1.2 },
    "meters": [{ "meterType": "CHECK_RUN", "measures": { "...": "..." } }]
  }],
  "pagination": { "nextId": null, "length": 1 },
  "usageTermsId": "usage-terms-id",
  "period": {
    "from": "YYYY-MM-DD",
    "to": "YYYY-MM-DD",
    "interval": "month",
    "groupBy": "account,checkType"
  },
  "warnings": [{ "code": "PARTIAL_WINDOW", "message": "..." }]
}
```

- `summary` JSON has no organization name, contract dates, or credit budget. Join `summary.usageTermsId` to `terms.id` for those fields.
- Select meter entries by the `meterType` discriminator (`CHECK_RUN` or `AI_INVOCATION`), never by array position.
- Nullable values include terms credit budget/rates, `credits.used`, `credits.percentOfBudget`, `projections.remainingCredits`, and projected window values such as `projectedWeeksUntilExhausted`. Treat `null` as unknown, not zero.
- Only `series` carries warnings. JSON returns `warnings: [{code, message}]`, while table/Markdown views print each warning message with its literal code. Preserve `PARTIAL_WINDOW`, `USAGE_TERMS_FLAGGED`, and `UNKNOWN_BUDGET`; `terms` and `summary` carry none.

## Terms and historical contracts

An explicit `--to YYYY-MM-DD` selects the usage terms covering that inclusive date; it does not name a usage-terms ID.

```bash
npx checkly account usage terms --to 2026-03-31 --output json
```

Interpret `NO_USAGE_TERMS` based on how the command was called:

- With explicit `--to`: that date is outside the account's known terms. Omit `--to` once to inspect current contract dates when available, then choose a covered date. Do not infer that the organization has never had a contract from one uncovered historical date.
- Without explicit `--to`: no current terms cover the active account. Stop probing arbitrary dates and use `npx checkly account plan` for plan or entitlement questions.

## Summary filters

```bash
npx checkly account usage summary \
  --from 2026-01-01 \
  --to 2026-01-31 \
  --account-id <account-id> \
  --check-type API \
  --output json
```

- Dates are inclusive and must use `YYYY-MM-DD`; `--from` cannot be after `--to`.
- Repeat `--account-id` and `--check-type`, or provide comma-separated values.
- Supported check types are `API`, `BROWSER`, `HEARTBEAT`, `MULTI_STEP`, `PLAYWRIGHT`, `TCP`, `ICMP`, `DNS`, `URL`, `GRPC`, `SSL`, `TRACEROUTE`, and `AGENTIC`.
- JSON summary output is the raw API summary. Human-readable output performs an extra terms lookup to add the organization name and budget.

## Series grouping, warnings, and pagination

```bash
npx checkly account usage series \
  --from 2026-01-01 \
  --to 2026-03-31 \
  --interval week \
  --group-by account,checkType \
  --account-id <account-id> \
  --limit 100 \
  --output json
```

- `--interval` accepts `total`, `day`, `week`, or `month`; the default is `day`.
- `--group-by` accepts `account`, `checkType`, or `account,checkType`; the default is `account,checkType`.
- `--limit` must be between 1 and 500; the default is 100.
- JSON output always includes `pagination.nextId` as `string | null`. Continue only when it is non-null; never pass `--cursor null`.
- Repeat every original date, filter, grouping, interval, and limit flag when adding `--cursor <nextId>`. Changing any resolved query parameter invalidates the cursor.

Example continuation:

```bash
npx checkly account usage series \
  --from 2026-01-01 \
  --to 2026-03-31 \
  --interval week \
  --group-by account,checkType \
  --account-id <account-id> \
  --limit 100 \
  --cursor <non-null-nextId> \
  --output json
```

## Troubleshooting

| Signal | Meaning and next action |
|---|---|
| HTTP `401` / "requires a user or service API key" | This is the blanket message for every unauthorized usage response, including revoked credentials, an incorrect `CHECKLY_ACCOUNT_ID`, an expired login, or a rejected legacy key. Run `npx checkly whoami` first, then use `checkly-auth` to repair the active user/service credential. |
| HTTP `403` | Usage requires Owner or Admin on the active account. `whoami` does not show role; use `npx checkly members --role owner --status active --output json` and `npx checkly members --role admin --status active --output json`, match the current identity, and use `npx checkly switch --account-id <account-id>` if the authorized role is on another account. |
| `NO_USAGE_TERMS` | With explicit `--to`, choose a date inside known terms. Without explicit `--to`, use `account plan` instead of probing dates for plan/entitlement questions. |
| `USAGE_TERMS_CONFLICT` | Choose a `--to` date covered by only one contract. |
| `ACCOUNT_NOT_IN_USAGE_TERMS` | Drop the account filter or correct `--account-id` to an ID in `terms.accounts[]`; changing only the date does not fix account membership. |
| `INVALID_CURSOR` | Re-run page one with the same explicit `--from`, `--to`, and all other flags, then use its newly returned non-null cursor. |
| `INVALID_RANGE` | Preserve the API message and correct the reported range problem. |
| `USAGE_STORE_UNAVAILABLE` | Preserve the error and retry later; do not infer zero usage. |
| `--to must be a valid calendar date...` / `--from must be a valid calendar date...` | Use a real calendar date in `YYYY-MM-DD`; values such as `2026-02-30` fail local validation. |
| `--from must be on or before --to.` | Correct the local range order before retrying. |

## Related Skills

- See `checkly-auth` for current user/service API keys, browser login, account switching, and credential troubleshooting.
- See `checkly-members` to verify Owner/Admin membership on the active account.
- See `checkly-checks` before triggering `checks run`, which consumes live account usage and may send alerts.
