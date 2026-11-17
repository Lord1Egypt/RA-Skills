---
name: ctyun-analyze-billing
description: Use when users ask to inspect, explain, reconcile, verify, or analyze CTYUN\天翼云 bills, charges, refunds, adjustments, product or resource costs, usage, billing-period changes, or dialogue billing reports through ctyun-cli.
---

# CTYUN Billing Analysis

Use fields returned by a bill API as bill facts. For every calculation or resource match, state the input, scope, and source. If data is missing, say “not retrieved” or “cannot determine.” Do not guess.

## Safety rules

- Run read-only Actions only. Do not change resources, purchase, renew, or refund.
- Add `--invoke-source ctyun-analyze-billing` only when this Skill runs a concrete product Action, such as `bill QueryMonthlyBillSummary`. Put this global flag before the product and Action. Do not add it to `version`, product help, Action help, or commands the user runs personally.
- Never run `ctyun-cli configure`, ask for credentials, put real keys on a command line, or enable `--log`.
- Do not show raw bill responses or save real bills in tests, source control, cross-session caches, or external services.
- Use `bill` first. This is a preferred route, not the only route. Check local help before using a new Action.
- Get user approval before expanding the account, project, product, region, resource, time, or verification scope.

Read [privacy policy](references/privacy-policy.md) before real queries. Read [troubleshooting](references/troubleshooting.md) when a command fails.

## Required tool: ctyun-cli

`ctyun-cli` is required. Without a working CLI and local credentials set up by the user, do not use web pages, guessed APIs, or billing conclusions. First run:

```text
ctyun-cli version
ctyun-cli --help
```

If either command fails, read [install ctyun-cli](references/install.md). The agent may install it with an official method only when the user asks or approves. After installation, the user must personally run `ctyun-cli configure`. The agent must not run it, type values into it, or receive credentials.

## Workflow

1. Set the billing period or date range, filters, question, and money basis. Keep the original field name when `amount`, `payableAmount`, or `price` is unclear.
2. Read [bill Actions](references/bill-actions.md) and [query catalog](references/query-catalog.md). Choose the smallest `bill` query that can answer the question. For an Action not in the list, run `ctyun-cli bill --help` and `ctyun-cli bill <Action> --help`. Check that it is read-only and confirm its scope, flags, pagination, and response fields.
3. Read [evidence policy](references/evidence-policy.md). Use P1 only when the bill does not explain a charge, the user asks for a check, or there is a dispute. Limit each resource query with a bill-derived `resourceId`, region, project, order, or time. Use P2 only when P0/P1 is not enough or the user asks.
4. Check whether all pages were returned. If not, do not claim a full check. If bill and resource data disagree, the bill API is the source of truth. Stop when the question is answered, no useful query remains, an ID is missing, or the next query would expand the scope.
5. Read [dialogue report specification](references/report-spec.md). Show only the needed redacted result. Label each important amount or conclusion as `Direct bill API value`, `Checked calculation`, `Partial data`, or `Cannot determine`.

## Reference navigation

- [bill Actions](references/bill-actions.md): choose or find a bill Action.
- [query catalog](references/query-catalog.md): flags and pagination hints.
- [evidence policy](references/evidence-policy.md): resource checks, money fields, conflicts, and pagination.
- [install ctyun-cli](references/install.md): CLI is missing or PATH does not work.
- [privacy policy](references/privacy-policy.md): before real queries and output.
- [dialogue report specification](references/report-spec.md): report content.
- [troubleshooting](references/troubleshooting.md): CLI, permission, field, pagination, or money issues.
