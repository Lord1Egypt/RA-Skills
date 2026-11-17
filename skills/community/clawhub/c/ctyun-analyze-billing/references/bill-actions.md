# Bill Actions and Runtime Discovery

This list contains common fast paths. It is not the only set of CLI Actions you may use. Prefer `bill` because it is the source of truth for charges that already happened and usually needs fewer calls. Do not call every Action before you know it is needed.

## Routing

| Intent | Preferred Action | Start with |
| --- | --- | --- |
| Consumption, refund, adjustment summary | `QueryMonthlyBillSummary` | `--billingCycleId` |
| Product cost | `QueryProductCycleBill` | billing cycle plus pagination |
| Resource cost | `QueryResourceCycleBill` | billing cycle plus pagination |
| Resource bill detail | `QueryResourceDetailBill` | billing cycle plus pagination; add bill-derived resource filter when possible |
| Usage by cycle | `QueryUsageCycleBill` | recheck help because required identity flags are version-sensitive |
| Usage detail | `QueryUsageDetailBill` | billing cycle plus pagination |
| On-demand transactions | `QueryQueryBillOnDemandFee` | billing cycle; paginate when the response declares a total |

Use the flags in [query-catalog.md](query-catalog.md), but local help is the source of truth. `isZeroFileter` and `groupByonDay` are the current CLI spellings; do not change them.

## Execution contract

1. Add `--invoke-source ctyun-analyze-billing` only when this Skill runs a concrete product Action. Place it before `bill` and the Action. Do not add it to `version`, product help, or Action help commands.
2. Run `ctyun-cli bill <Action> --help` before the first real query when the CLI version has changed, a flag fails, or the Action is not in this list.
3. Supply credentials through the user's existing local configuration. Never put AK/SK in the command.
4. Use JSON output. Do not enable `--log`.
5. Start with the smallest useful scope and a small page size when the response shape is unknown.
6. Complete pagination for full verification. For quick analysis, disclose partial coverage.
7. Retain source Action, row index, declared total, billing scope, and independent money fields.
8. Stop as soon as the locked question is answered.

Use this shape for a real bill Action:

```text
ctyun-cli --invoke-source ctyun-analyze-billing bill <Action> <Action flags>
```

## Bill Actions not in this list

When the fast paths do not fit, run:

```text
ctyun-cli bill --help
ctyun-cli bill <Action> --help
```

Confirm that the Action is read-only, the scope is approved, the flags and pagination are clear, and the response has the needed evidence. You may use a checked read-only bill Action right away. Add it to this list later only if it helps future routing. If its behavior or change risk is unclear, do not run it.

If the Action has a new response shape or fields, do not force it into an old
mapping. Use a small scoped response and a one-time local extraction that keeps
the documented source field names. You do not need to update this list before
using a safe, checked Action.

## Pagination and empty results

Compare the unique rows collected with the total count returned by the API. An empty page means only that this exact scope has no rows; it does not prove that the account has no spend. Keep refunds, adjustments, and zero-value rows.
