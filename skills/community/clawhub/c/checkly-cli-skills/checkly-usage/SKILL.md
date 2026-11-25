---
name: checkly-usage
description: Inspect Checkly account plans, entitlements, feature limits, plan limits, private-location entitlements, contract credits, self-service USD usage, projections, and overage spending caps. Use when selecting usage filters, interpreting machine output, or reviewing an explicitly authorized spending-cap set or removal. Triggers on checkly account plan, checkly account usage, checkly account spending-cap, usage terms, usage summary, usage series, per-period consumption, private-location availability, spending cap.
---

# Checkly account plan, usage and spending cap

Use `account plan` for account entitlements and limits. Use `account usage` for contract or self-service terms, measured consumption and projections. Use `account spending-cap` to inspect overage limits; changes require the authorization workflow below. Confirm the effective account with `npx checkly whoami --output json` before interpreting results. Usage requires a current user/service credential with `usage:read` permission; legacy account keys are not accepted.

Check the [CLI compatibility requirements](references/compatibility.md) before using optional projection IDs, unit-aware usage fields, the combined pricing-rule keys, or spending-cap commands. These are source-backed semantics, not binary help captures. Immutable sources: [usage types and endpoints](https://github.com/checkly/checkly-cli/blob/c58d58c171152336dfc87f2e7b77e742f9b4ffa5/packages/cli/src/rest/usage.ts), [projection command](https://github.com/checkly/checkly-cli/blob/c58d58c171152336dfc87f2e7b77e742f9b4ffa5/packages/cli/src/commands/account/usage/projections.ts), and [usage formatting](https://github.com/checkly/checkly-cli/blob/c58d58c171152336dfc87f2e7b77e742f9b4ffa5/packages/cli/src/formatters/usage.ts).

## Command map

| Command | Purpose | Default output |
|---|---|---|
| `account plan [KEY]` | Plan, add-ons, entitlements and location limits | `table` |
| `account usage terms` | Paginated list of terms, optionally overlapping dates | `table` |
| `account usage term <id>` | One term UUID, pricing rules and covered accounts | `detail` |
| `account usage summary` | Usage totals, pricing breakdowns and coverage gaps | `detail` |
| `account usage series` | Per-period rows with composable dimensions | `table` |
| `account usage projections [id]` | Project a term UUID, or the term in force today | `detail` |

All accept `--output json` or `--output md` (`-o` is the short flag); table-default commands also accept `table`, detail-default commands accept `detail`. Results go to stdout and diagnostic errors to stderr. Invalid inputs exit 2; runtime failures exit 1.

## Spending cap: inspect, authorize, preview, read back

The show command is `account spending-cap` (no `show` subcommand). It uses `GET /v1/billing/spending-cap`. `set <dollars>` and `remove` first GET the current cap, then, after confirmation, PUT the same endpoint with `{ spendingCapCents: <integer> }` or `{ spendingCapCents: null }`. Removal is not DELETE. All three accept `--output`/`-o` with `detail` (default), `json`, or `md`; mutations also accept `--dry-run` and `--force`/`-f`.

```bash
# Read-only inspection; choose and verify the effective account first.
npx checkly whoami --output json
npx checkly account spending-cap --output json
```

Before any write, obtain explicit authorization for the **exact account ID and exact dollar value**, or for **removal of that account's cap**. A request to inspect usage, a generic cost-saving request, or CLI confirmation metadata is not authorization. Set `CHECKLY_ACCOUNT_ID` before starting each process and verify `whoami`; it overrides the saved account. Spending-cap commands have no `--account-id` flag. Usage's `--account-id` only filters report rows.

After the user selects a change, preview `account spending-cap set <dollars> --dry-run` or `account spending-cap remove --dry-run`. These contact the API to read current state but do not write. Review the preview with the user, including service impact. Only after exact authorization, apply that same command/account without `--dry-run`, confirming interactively or using `--force`. Never blindly execute a returned `confirmCommand`: verify the command, value and effective account still match approval. Afterwards, read `account spending-cap --output json` again in that account and verify the stored cents or null; report the measurement time and standing separately. A successful PUT is not standing readback.

- Dollars range from **0 to 10000 inclusive**, with at most two decimals; `12.5` and `12.50` are valid. Parsing trims surrounding whitespace and converts decimal digits to integer cents. Negative values, exponent notation, `$` prefixes, `.5`, `5.`, and excess precision are invalid (exit 2).
- Zero allows no overage: checks stop once included runs are exhausted. Lowering the cap to or below positive overage already measured can stop checks immediately. Removing it leaves overage uncapped. Treat these as billing and monitoring changes even though `set` metadata says `destructive: false`.
- `--dry-run` takes precedence over `--force`, prints JSON `status: "dry_run"` and exits 0. Unconfirmed agent/CI mutations print a JSON `confirmation_required` preview and exit 3. Unrecognized runtimes, including plain scripts and cron jobs, fall back to interactive mode: confirmation can wait for input or cancel with exit 0 without writing. Unattended callers should explicitly set `CHECKLY_CLI_MODE=agent` before launch (accepted values: `interactive`, `ci`, `agent`); mode selection does not authorize a write. Exit 0 alone is not evidence of a mutation: require the PUT result or success message plus exact-account readback. Previews are distinct from successful results, even with `--output json`.
- Show JSON is the raw GET response: `spendingCapCents` plus `standing`. Successful mutation JSON is the PUT response (`spendingCapCents`), without a fresh standing. Human mutation output is a success message. Results and JSON (`dry_run` / `confirmation_required`) previews go to stdout; the interactive preview, prompts and diagnostics go to stderr; runtime failures exit 1.
- `spendingCapCents: null` means no cap; `0` means no overage. `standing: null` means unmeasured or a plan without overage, **not zero spend**. A measured standing includes `measuredAt`, `pools` keyed by product (`used`, `included`, `overageRuns`, `overageCents`), aggregate `overageCents`, and nullable `limit` (`capCents`, `state`, `closeAtCents`). States are `UNDER`, `CLOSE`, `REACHED`; only `REACHED` reports checks stopped. Do not infer a fixed warning threshold: use `closeAtCents`.
- Amounts are US cents; overage may include fractional cents. Human spending-cap output rounds dollars to two decimals; JSON retains API precision. With no standing, human output omits checks-stopped status; with no limit, it omits cap status.
- GET needs `billing:read`; PUT needs `billing:update` (and the CLI's preceding GET still needs read access). A 401 explains that user/service keys are required and legacy account keys are rejected. A normal 403 points to billing permission and self-serve billing; account-inaccessible errors retain their account diagnosis. A 409 rejects ineligible plans such as prepaid or contract. Do not change credentials, roles or plans to bypass these errors.

Immutable sources: [commands](https://github.com/checkly/checkly-cli/tree/c58d58c171152336dfc87f2e7b77e742f9b4ffa5/packages/cli/src/commands/account/spending-cap), [show](https://github.com/checkly/checkly-cli/blob/c58d58c171152336dfc87f2e7b77e742f9b4ffa5/packages/cli/src/commands/account/spending-cap.ts), [REST types](https://github.com/checkly/checkly-cli/blob/c58d58c171152336dfc87f2e7b77e742f9b4ffa5/packages/cli/src/rest/spending-cap.ts), [validation and warnings](https://github.com/checkly/checkly-cli/blob/c58d58c171152336dfc87f2e7b77e742f9b4ffa5/packages/cli/src/helpers/spending-cap.ts), [confirmation behavior](https://github.com/checkly/checkly-cli/blob/c58d58c171152336dfc87f2e7b77e742f9b4ffa5/packages/cli/src/commands/authCommand.ts), and [mode detection](https://github.com/checkly/checkly-cli/blob/c58d58c171152336dfc87f2e7b77e742f9b4ffa5/packages/cli/src/helpers/cli-mode.ts).

## Account plan

```bash
npx checkly account plan --output json
npx checkly account plan --search browser --output json
npx checkly account plan <ENTITLEMENT_KEY> --output json
npx checkly account plan --disabled --output table
```

`--type` accepts `metered` or `flag`. A positional key cannot be combined with `--type`, `--search` or `--disabled`. An unknown key exits 1. Unfiltered JSON has `plan`, `planDisplayName`, `addons`, optional `locations`, and `entitlements[]`. Filtered JSON is an entitlement array; a key lookup returns one object. Inspect `locations.all[].available` and `locations.maxPerCheck` for location limits.

## Select terms and dates

```bash
npx checkly account usage terms --from 2026-01-01 --to 2026-03-31 --output json
npx checkly account usage term <term-uuid> --output json
npx checkly account usage summary --from 2026-01-01 --to 2026-03-31 --usage-terms-id <term-uuid> --output json
npx checkly account usage series --from 2026-01-01 --to 2026-03-31 --group-by account,checkType --include runs --output json
npx checkly account usage projections <term-uuid> --as-of 2026-03-31 --output json
```

Dates are inclusive UTC `YYYY-MM-DD` calendar dates, with `from <= to`. For `terms`, neither date has a default: the range selects **all overlapping terms**, not one contract covering the end date. For `summary`/`series`, `--to` defaults to today and `--from` to the earliest selected usage start, or the end date. Pin both dates for comparisons and pagination.

`projections` without an ID calls `GET /v2/usage/projections` with no term selector: the API chooses the term in force **today**, independently of `--as-of`. An explicit UUID is sent as the `usageTermsId` query parameter, not a term-scoped URL. Human output attempts to look up the returned term name and falls back to its ID; JSON returns the projection directly without a name lookup. If no term is in force, list `account usage terms` and select an explicit ID.

`projections --as-of` defaults to **yesterday UTC**. Today and future dates are rejected: projections use a completed UTC day. Report the selected term and as-of date alongside any estimate; do not describe a projection as measured usage.

## Range and series flags

`summary` and `series` accept repeated or comma-separated `--usage-terms-id` UUIDs, `--account-id` GUIDs and `--pricing-rule` keys (up to 100 values per list). `--account-id` filters covered accounts; it does not switch authentication. Set `CHECKLY_ACCOUNT_ID` before launching the CLI to select the authenticated account.

Pricing keys: `apiChecks`, `multistepChecks`, `browserChecks`, `playwrightCheckSuites`, `apiAndMultistepChecks`, `browserAndPlaywrightChecks`, `uptimeMonitors`, `aiInvocations`, `statusPages`, `statusPageAdditionalServices`, `statusPageAdditionalSubscribers`, `additionalSms`, `additionalPhoneAlerts`.

Migration warning: `--check-type` was removed and is rejected. Select charges with `--pricing-rule`, or break them down with `series --group-by checkType`.

| Series flag | Values |
|---|---|
| `--interval` | `total`, `day` (default), `week`, `month` |
| `--group-by` | Comma-separated `account`, `usageTerm`, `pricingRule`, `checkType`; `none` for no grouping. Default `account,checkType`. |
| `--include` | `runs`, `calculations`, or both; repeat or comma-separate. |
| `--limit`, `-l` | 1–500, default 100; also on `terms`. |
| `--cursor` | Nonempty next-page cursor; also on `terms`. |

Continue only when `pagination.nextId` is non-null. Reuse effective dates and every selection, grouping, include, interval and limit from page one (or the printed continuation command). Do not pass the string `null` as a cursor.

## JSON contract

Read `unit` before interpreting amounts: `credits` for contract terms, `usdCents` for self-service terms. Summary/series `unit` may be null; do not invent a currency or combine unlike units. Human usage output converts cents to USD with up to six decimal places (credits use up to four), while JSON retains the API numbers. The old credit-total fields were removed/renamed, not retained as aliases; migrate consumers using this mapping (see [compatibility requirements](references/compatibility.md) for the release boundary):

| Removed field | Current field |
|---|---|
| `creditBudget` | `unitBudget` |
| `creditsUsed` | `unitsUsed` |
| `remainingCredits` | `unitsRemaining` |
| `budgetedDailyCredits` | `budgetedDailyUnits` |
| `averageDailyCredits` | `averageDailyUnits` |
| `projectedCreditsAtContractEnd` | `projectedUnitsAtContractEnd` |
| `projectedRemainingCredits` | `projectedUnitsRemaining` |

Pricing-rule fields `credits`, `price.annualCredits`, `block.annualCredits`, and calculation rate fields `appliedDailyCredits`/`appliedDailyCreditsPerBlock` retain their names but are interpreted in the term's unit. These are object fields, not `--pricing-rule` values or `breakdown[].pricingRuleKey` identifiers. On `usdCents` terms their human labels say price and values are divided by 100; contract-only standard/premium conversion rows are hidden. Do not rename these remaining rate fields or confuse a pricing rule's quantity unit (such as runs) with the term's monetary unit.

These are abbreviated structural examples, not captured responses:

```jsonc
// terms: list wrapper; term <id>: one object from data
{
  "data": [{
    "id": "term-uuid", "name": "Organization",
    "accounts": [{ "id": "account-guid", "name": "Account" }],
    "contractStartDate": "2026-01-01", "contractEndDate": "2026-12-31",
    "usageStartDate": "2026-01-01", "unit": "credits", "unitBudget": 100000,
    "standardCreditsPerUnit": 1, "premiumCreditsPerUnit": 2,
    "packageModel": "credits", "pricingRules": {}
  }],
  "pagination": { "nextId": null, "length": 1 }
}
// summary
{
  "period": { "from": "2026-01-01", "to": "2026-03-31" },
  "usageTermsIds": ["term-uuid"], "unit": "credits",
  "totals": { "unitsUsed": 123 },
  "breakdown": [],
  "coverage": { "gaps": [] }
}
// series
{
  "data": [{
    "periodStart": "2026-01-01", "periodEnd": "2026-01-01",
    "dimensions": { "accountId": "account-guid", "checkType": "API" },
    "unitsUsed": 12, "contributions": []
  }],
  "pagination": { "nextId": null, "length": 1 },
  "period": { "from": "2026-01-01", "to": "2026-03-31" },
  "usageTermsIds": ["term-uuid"], "unit": "credits",
  "interval": "day", "groupBy": ["account", "checkType"],
  "coverage": { "gaps": [] }
}
```

- `summary.totals.unitsUsed` is nullable. Summary has no `percentOfBudget`, meters or projections. Its `breakdown[]` includes term ID, pricing-rule key, period, pricing rule, calculations and units used, with optional account ID.
- `usageTermsIds` is a list on summary/series. Join each ID to `term <id>` or `terms.data[]`; do not assume one contract.
- Series `dimensions` carries selected account, term, pricing-rule and check-type dimensions. Rows use `unitsUsed`, not nested credits. `interval` and `groupBy` are top-level, with `groupBy` an array.
- `runs` appears only with `--include runs` and can be null; available counters include `totalRuns`, `finalRuns`, `retryRuns`, `cancelledRuns`, `degradedRuns`, `failedRuns`, `errorRuns`, `abortedRuns`, and `overMaxResponseTimeRuns`. `--include calculations` adds pricing details to contributions.
- `coverage.gaps[]` contains `{ from, to }` ranges; preserve gaps when summarizing coverage. It replaces the old series warnings array. Treat null units/budgets/rates/projections as unknown, never zero.
- Projections are a separate response: singular `usageTermsId`, `asOf`, nullable `period`, `weeksSinceStart`, `weeksRemaining`, `unit`, `unitsUsed`, `unitsRemaining`, `budgetedDailyUnits`, and `windows` (`sinceStart`, `last30Days`, `last7Days`, `last1Day`). Each window includes nullable `period`, `observedDays`, `averageDailyUnits`, `unitsUsed`, `projectedUnitsAtContractEnd`, `projectedUnitsRemaining`, `projectedPercentAtContractEnd`, `projectedAnnualPercentOfBudget` and `projectedWeeksUntilExhausted`. Projection values can be null.

## Diagnose usage access

The [Usage API](https://www.checklyhq.com/docs/api-reference/usage/overview/) requires `usage:read` (**View usage**). Owner and Admin have it by default. User API keys inherit their user's account role; service API keys use the role assigned to the key, not the creator's role. Where custom roles are enabled, they can grant this permission too. See [permission names](https://www.checklyhq.com/docs/admin/team-management/permissions#usage) and [API-key roles](https://www.checklyhq.com/docs/admin/creating-api-key/).

```bash
# Confirm the effective identity/account first; whoami does not expose a role.
npx checkly whoami --output json
# Check built-in active member roles; match the returned identity, not any admin.
npx checkly members --role owner --status active --output json
npx checkly members --role admin --status active --output json
```

These member lists diagnose built-in human membership, not the effective permissions of a service key or a custom role. Follow any non-null next-page cursor before concluding that a member is absent. For a service key, have an authorized account administrator inspect its assigned role in Account Settings > API keys, without revealing the key. For a custom role, inspect **View usage** under Account Settings > Roles (only on enabled accounts), or ask the owner/admin to confirm it. Do not change roles or create/rotate keys just to troubleshoot.

If the authorized role belongs to another account, deliberately select that account for a **new CLI process**. Set or correct `CHECKLY_ACCOUNT_ID` before launch (or remove an unintended override before `npx checkly switch --account-id <account-id>`); then rerun `whoami`. A saved account switch cannot override a still-set environment selection. A successful `whoami` does not prove usage permission. A 401 requires credential/account diagnosis; a 403 or bare permission failure requires checking the effective role and `usage:read`, rather than repeatedly logging in.

## Troubleshooting

| Signal | Action |
|---|---|
| `NO_USAGE_TERMS` | List terms and choose available term IDs or a covered date range; a missing detail/projection ID does not mean no contracts exist. |
| `USAGE_TERMS_CONFLICT` | Choose non-overlapping terms with `--usage-terms-id` or narrow the range. |
| `ACCOUNT_NOT_IN_USAGE_TERMS` | Correct the filter using the term's covered accounts. |
| `INVALID_CURSOR` | Restart with pinned effective dates and all original flags. |
| `INVALID_RANGE` | Correct the range described by the API. |
| `USAGE_STORE_UNAVAILABLE` | Retry later; do not infer zero usage. |
| Unauthorized / inaccessible account | Verify the effective account and current user/service credentials without logging keys. |
| HTTP 403 / bare permission failure | Follow [Diagnose usage access](#diagnose-usage-access): confirm the effective account, user membership or service-key role, and `usage:read`; Owner/Admin have it by default, and enabled custom roles can grant it. |

See `checkly-auth` for account overrides and `checkly-members` for membership inspection.
