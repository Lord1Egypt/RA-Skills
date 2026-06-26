---
name: feature-flag-cleanup
description: Audit feature flag debt across LaunchDarkly, Unleash, Flagsmith, GrowthBook, Split, and home-grown flag systems. Detects stale flags (older than 90 days, fully rolled out, no toggle activity), classifies them by risk (kill-switch vs experiment vs permission vs ops toggle), tags owners from git blame and CODEOWNERS, generates removal pull requests ordered by safety, and produces a four-week cleanup playbook with rollback plans. Use when asked to find dead flags, reduce flag debt, plan a flag cleanup sprint, write a flag-removal PR, decommission a vendor flag service, or audit flag usage in a monorepo. Triggers on "feature flag", "feature toggle", "launchdarkly", "unleash", "flagsmith", "growthbook", "split.io", "stale flag", "dead flag", "flag debt", "flag cleanup", "flag audit", "kill switch", "rollout", "flag retirement".
metadata:
  tags: ["feature-flags", "launchdarkly", "unleash", "flagsmith", "growthbook", "split", "tech-debt", "code-cleanup", "refactoring", "devops", "platform-engineering"]
---

# Feature Flag Cleanup

Audit and retire stale feature flags across a codebase and a flag service (LaunchDarkly, Unleash, Flagsmith, GrowthBook, Split, custom). Produces a ranked removal plan, owner-tagged tickets, removal PRs grouped by risk, and a four-week cleanup sprint. Acts as a platform engineer who has decommissioned thousands of flags without breaking production.

## Usage

Invoke this skill when feature flag debt is slowing engineering down: builds carry stale toggles, code paths exist for experiments that ended a year ago, the LaunchDarkly bill is climbing, or a refactor is blocked by unread flags.

**Basic invocation:**
> Audit our LaunchDarkly account and our monorepo for stale flags
> We have 1,200 flags in Unleash — find the dead ones
> Write a removal PR for the `new-checkout-v2` flag

**With context:**
> Here's our LD export and the code grep — order removals by risk
> We're moving off Split.io to GrowthBook — what flags die in the migration?
> Audit only the flags owned by my team (CODEOWNERS: payments)

The agent produces a stale-flag inventory, a four-week cleanup schedule, removal PRs in safety order, and a per-owner ticket list.

## How It Works

### Step 1: Inventory The Flag Estate

The agent first builds a complete inventory across two surfaces and joins them:

| Surface | What It Holds | How To Pull |
|---------|---------------|-------------|
| **Flag service** | Targeting rules, rollout %, last-modified date, evaluation count | LaunchDarkly REST API `/api/v2/flags`, Unleash `/api/admin/features`, Flagsmith `/api/v1/features/`, GrowthBook `/api/v1/features`, Split `/internal/api/v2/splits` |
| **Codebase** | Flag references in source, configs, tests | `git grep`, AST parse, language-specific clients (`useFeatureFlag`, `client.boolVariation`, `unleash.isEnabled`) |
| **Telemetry** | Production evaluation counts per flag per day | Datadog, Honeycomb, vendor evaluation logs, OpenTelemetry traces |
| **Ticket system** | Originating ticket, intended sunset date | Jira `flag:` label, Linear cycle search |

The join key is the flag's `key` (string id). Any flag that exists in only one surface is suspect — code references with no service definition are dead code; service definitions with no code references are dead config.

### Step 2: Classify Every Flag

Not all flags retire the same way. The agent assigns one of five **types** before deciding what to do:

| Type | Lifetime Expectation | Cleanup Default |
|------|---------------------|-----------------|
| **Release toggle** | Days to weeks during a rollout | Remove once 100% on for 30 days |
| **Experiment** | One experiment cycle (2-8 weeks) | Remove once analysis is shipped, winner picked |
| **Permission / entitlement** | Permanent | Migrate to authz system, then remove |
| **Ops / kill switch** | Permanent | Keep but document; review yearly |
| **Config / parameter** | Permanent | Migrate to config service if static, remove if dynamic decision is gone |

A flag's *type* is rarely tagged at creation — the agent infers from name patterns (`enable_`, `kill_`, `experiment_`, `tier_`), targeting rules (percentage rollout vs user-list vs segment), and evaluation patterns (steady-state vs spiking on deploy days).

### Step 3: Detect Staleness

The agent applies a layered staleness ruleset. A flag must trip **at least two rules** to be marked stale (single-rule failures produce a "watch list", not a removal).

**Time rules:**

```
R1. created_at older than 90 days
R2. last_modified older than 60 days (rules untouched)
R3. last_evaluation older than 30 days (no traffic)
R4. originating Jira ticket closed >180 days ago
```

**State rules:**

```
R5. served value is 100% (or 0%) for 30+ consecutive days
R6. all targeting rules collapse to a single variant (no branching)
R7. zero overrides, zero environment-specific differences
R8. variant served matches default for environment
```

**Code rules:**

```
R9. flag key not present in main branch (only in deleted branches / archived dirs)
R10. all code references are inside a single if branch with no else
R11. all references are tests (no production callsite)
R12. references exist only in disabled feature folders
```

**Service rules:**

```
R13. flag is archived in service but still referenced in code
R14. flag is in service but never linked to code (orphan)
R15. flag references a deleted segment / user list
R16. flag's prerequisites form a cycle or reference deleted flags
```

A removal candidate scores `count(rules_tripped)` plus a risk modifier (see Step 4). Anything ≥ 4 is a strong removal; 2-3 is staged with extra verification.

### Step 4: Risk Classification (Severity Matrix)

Each flag gets a removal-risk grade. Risk is independent of staleness — a stale flag can still be high-risk to remove if the wrong default ships.

| Grade | Criteria | Removal Approach |
|-------|----------|------------------|
| **R0 — Trivial** | Test-only references, dev-only flag, zero prod traffic in 90d | Single PR, batch with siblings |
| **R1 — Low** | Release toggle 100% on 60+ days, simple boolean, single owner | One PR per flag, standard review |
| **R2 — Medium** | Touches a paid feature, multiple owners, has variants beyond on/off, evaluated >1k/day | One PR per flag, two reviewers, deploy in own release window |
| **R3 — High** | Permission/entitlement, billing-adjacent, payment path, auth path | Migrate before remove. Owner sign-off required, integration tests, dark-launch the removal |
| **R4 — Critical** | Kill switch, regulatory, data residency, encryption toggle | Keep. Document and review yearly. Removal blocked unless replacement is in place. |

The agent never auto-generates a removal PR for R3 or R4 — those produce migration tickets instead.

### Step 5: Owner Tagging

Removals stall when nobody is on the hook. The agent assigns each flag exactly one owner using a fallback chain:

```
1. Service-side `tags` or `maintainer` field          (LaunchDarkly tags, Unleash project)
2. Originating Jira/Linear ticket assignee
3. CODEOWNERS for the file containing the most references
4. `git log --follow` first author of the introducing commit
5. `git blame` on the line of the most recent flag check
6. Team channel mapping (#payments → @payments-leads)
```

The agent emits a per-owner queue so each engineer sees only their flags. Bulk emails to "engineering@" produce zero cleanup; per-owner tickets with a 2-week SLA produce 70%+ completion.

### Step 6: Generate Removal Recipes

For each removable flag the agent emits a deterministic recipe by language and client. The pattern always:

1. Replace the `if (flag) { A } else { B }` with the **winning** branch
2. Delete the dead branch and any helpers it called
3. Remove the flag-client import if it was the last reference in the file
4. Delete the flag's service definition (or archive it)
5. Drop tests for the dead branch; re-baseline snapshot tests
6. Remove documentation references (runbooks, ADRs, feature lists)

**Example — TypeScript / LaunchDarkly:**

```ts
// before
import { useFlags } from 'launchdarkly-react-client-sdk';
const { newCheckout } = useFlags();
return newCheckout ? <CheckoutV2 /> : <CheckoutV1 />;

// after (newCheckout was 100% on for 60 days)
return <CheckoutV2 />;

// then delete CheckoutV1.tsx, its tests, its CSS, and remove from routing
```

**Example — Go / Unleash:**

```go
// before
if unleash.IsEnabled("ff_async_export") {
    go runAsyncExport(ctx, req)
} else {
    runSyncExport(ctx, req)
}

// after
go runAsyncExport(ctx, req)

// then delete runSyncExport, delete its mock, prune the unleash strategy
```

**Example — Python / Flagsmith:**

```python
# before
if flagsmith.has_feature("legacy_pricing", default=False):
    price = legacy_price_engine(cart)
else:
    price = price_engine_v2(cart)

# after
price = price_engine_v2(cart)

# then drop legacy_price_engine module and its 14 fixture files
```

**Example — Custom DB-backed flag:**

```python
# before
if FeatureToggle.objects.get(key="multi_currency").enabled:
    currency = detect_user_currency(user)
else:
    currency = "USD"

# after
currency = detect_user_currency(user)

# then drop the FeatureToggle row, the migration to delete is M0142
```

### Step 7: Pull Request Strategy

The agent organizes PRs to balance reviewer load and blast radius:

- **Batch R0 trivial** — one PR per service or per directory, up to 20 flags. Single reviewer.
- **One PR per R1** — small, mechanical, easy revert. Title format: `chore(flags): remove ff_X (100% on since YYYY-MM-DD)`.
- **One PR per R2 with deploy gate** — merge during low-traffic window, watch error budget for 24h, document the rollback flag default.
- **R3 splits into two PRs:**
  - PR-1: Land the *replacement* (authz rule, config value, kill switch in new system) without touching the flag.
  - PR-2: Remove the flag once PR-1 has been in production for 7 days clean.

Every PR includes a **Rollback Plan** section. The agent generates it from the flag definition:

```markdown
## Rollback Plan
If incident: revert this commit. The previous behavior was the
`disabled` branch which called `legacy_pricing_engine`. That code
is preserved in commit abc1234 of branch `archive/ff-legacy-pricing`
for 90 days post-merge. After 90 days, recover from git history
via `git log --all --source -- legacy_pricing_engine.py`.
```

### Step 8: Gradual Rollback Plan

Even after removal, the agent leaves a **30-60-90 day safety net**:

| Day | Action |
|-----|--------|
| **0** | Merge removal PR. Tag the commit `flag-removed/ff_xxx`. Open a 30-day calendar reminder for the owner. |
| **7** | Verify error rate, latency, conversion metric vs baseline. If regression, the agent generates a re-introduction PR that restores the flag and pins it to the previous default. |
| **30** | Delete the flag definition in the service (was archived at PR merge). Drop the archive branch if no rollback called. |
| **60** | Review the removed-flags log; mark "permanent" in MEMORY. |
| **90** | Drop the flag from runbooks, dashboards, alerts. |

For R3 / R4 retentions, extend the windows: 14 / 60 / 120 / 180.

### Step 9: Service Provider Specifics

Each provider has its own retirement workflow. The agent uses the right API, the right resource hierarchy, and the right billing impact.

**LaunchDarkly:**

- API: `DELETE /api/v2/flags/{projKey}/{flagKey}` (archives by default; pass `?archived=true` to unarchive)
- Use **flag tags** liberally — `temporary`, `experiment`, `kill-switch` make Step 2 automatic going forward
- LD's **Code references** integration (via GitHub/GitLab) is the single highest-leverage tool — install before doing the audit
- LD bills per **MAU evaluated**, not per flag — removing a low-traffic flag saves nothing on the bill; removing a high-traffic experiment that's still 50/50 on a logged-in segment saves the most
- Use **Workflows** to schedule the staged rollback (e.g. archive after 30 days)

**Unleash:**

- Open-source, often self-hosted; cleanup recovers DB rows but not license cost
- Built-in **stale flag** UI under Project → Reports
- API: `DELETE /api/admin/features/{name}` (archives), then `DELETE /api/admin/archive/{name}` (hard delete)
- Strategies are independent objects — verify no other flag references the strategy before deleting it
- Unleash 5+ supports **Dependencies** between flags — break dependencies before deletion

**Flagsmith:**

- Per-environment overrides are common — verify all environments have collapsed to a single value before removal
- API: `DELETE /api/v1/projects/{id}/features/{id}/`
- **Segments** are project-scoped; orphaned segments accumulate fast — sweep them in the same audit
- Self-hosted Flagsmith persists evaluation logs only if the influxdb integration is enabled — without it, R3 (last_evaluation) is unreliable

**GrowthBook:**

- Experiment-first model; many flags are tied to a running experiment doc
- Closing the experiment doesn't delete the flag — explicitly archive after analysis
- API: `DELETE /api/v1/features/{id}` (requires admin role)
- The **Code references** scan in the GrowthBook proxy is opt-in; turn it on before audit

**Split.io:**

- "Splits" are the flag; "Treatments" are the variants
- Killing a split via UI sets it to a single treatment but does not remove from code — agent must still produce the code-removal PR
- API: `DELETE /internal/api/v2/splits/ws/{wsId}/{splitName}` (workspaces matter, easy to delete the wrong env)
- Split's **dynamic configurations** are JSON-typed — removal recipes for these inline the JSON value, not a boolean

**Custom / DB-backed flags:**

- Hardest case — no audit UI, no API. The agent generates SQL to find dead flags:
  ```sql
  SELECT key, MAX(updated_at)
  FROM   feature_toggles
  WHERE  key NOT IN ($referenced_keys_from_grep)
     OR  updated_at < NOW() - INTERVAL '180 days';
  ```
- Removal is a database migration plus a code change in the same PR
- Add a **flag definition test** that fails CI when a code reference exists without a DB row, and vice versa

### Step 10: Four-Week Cleanup Playbook

Cleanup as a one-off audit dies. Cleanup as a recurring sprint sticks. The agent emits a four-week schedule:

```
WEEK 1 — INVENTORY & BASELINE
Mon  Pull flag list from service API → CSV
Tue  git grep code references → join to CSV
Wed  Pull last 30d evaluation telemetry → join to CSV
Thu  Classify by type (R0-R4), tag owners, generate per-owner queue
Fri  Publish dashboard: total flags, removable count, debt $$ estimate

WEEK 2 — TRIVIAL & LOW (R0/R1)
Mon  Bulk-PR all R0 flags (test-only, dev-only)
Tue  Open R1 PRs in batches of 10 per team
Wed  Merge R0 batch (single reviewer), monitor CI
Thu  Merge R1 batch on standard review cadence
Fri  Service-side: archive the merged flags, refresh dashboard

WEEK 3 — MEDIUM (R2)
Mon  Per-flag PRs for R2; pair with feature owner
Tue  Schedule R2 deploys to low-traffic windows
Wed  Deploy first half, watch error budget for 24h
Thu  Deploy second half if green; revert plan exercised on any regression
Fri  Service-side cleanup; mark watch-period start date

WEEK 4 — HIGH (R3) MIGRATION + REPORT
Mon  R3 migration PRs land (NOT removals — replacements)
Tue  Replacement code burns in for the 7-day rule
Wed  Generate the 30/60/90 calendar reminders
Thu  Update runbooks, ADRs, onboarding docs to match new state
Fri  Post-mortem write-up: flags removed, $$ saved, debt remaining,
     and a date for the next quarter's audit
```

### Step 11: Prevention — Stop The Debt At The Source

Cleanup without prevention runs the same audit again next quarter. The agent emits a prevention pack:

- **Mandatory expiry date** at flag creation. Service-level enforcement: LaunchDarkly *Workflows*, Unleash *flag templates*, custom DB column `expires_at NOT NULL`.
- **PR template** for new flags: type, owner, expected sunset, kill-switch criteria, removal ticket linked.
- **CI lint**: a check that fails when a flag is created without an `expires_at`, or when the introducing PR has no linked removal ticket.
- **Quarterly audit cron** (the agent ships the script): runs the staleness rules and opens a tracking ticket per owner.
- **Flag SLO**: max 50 active flags per service (or N per 1k LOC). Breach blocks new flag creation in CI.
- **Onboarding doc**: every new engineer reads the "flags are debt by default" page before getting service-side write access.

## Worked Examples

### Example 1: 1,200-Flag LaunchDarkly Account Cleanup

**Inventory results:**

```
Total flags                    1,212
  - Active                       743
  - Archived (still in code)     204
  - Code-only orphans            265

By type:
  - Release toggle               612 (50%)
  - Experiment                   188 (15%)
  - Permission/entitlement       121 (10%)
  - Ops/kill                      94 (8%)
  - Unclassified                 197 (16%)

Staleness (≥2 rules tripped):    687 candidates (57%)
By risk:
  - R0 trivial                   142
  - R1 low                       312
  - R2 medium                    178
  - R3 high                       49
  - R4 critical                    6
```

**Plan:**

- Week 2: 142 R0 flags removed in 8 batched PRs. Engineering hours: ~12.
- Week 3: 312 R1 flags removed across 14 teams. Per-team queue, average 22 flags. Engineering hours: ~120 (org-wide, not per team).
- Week 4: 178 R2 staged across two release windows. Owner pairing required. Engineering hours: ~80.
- Quarter 2: 49 R3 migrations begin (not full removals).
- 6 R4 documented and parked.

Estimated savings: 38% reduction in flag count, ~$22k/yr LD cost reduction (based on MAU savings from the 89 high-traffic experiments retired), and ~3,400 LOC removed.

### Example 2: Single Flag Removal — `new_checkout_v2`

**Audit:**

```
Key:               new_checkout_v2
Service:           LaunchDarkly (project: web-app)
Created:           2025-01-12 (110 days ago)
Last modified:     2025-02-14 (rules frozen)
Rollout:           100% production for 84 days
Variants:          on / off
Code refs:         3 files, 7 callsites
  - src/checkout/route.tsx (4)
  - src/checkout/__tests__/route.test.tsx (2)
  - src/analytics/checkout.ts (1)
Telemetry:         184k evals/day, all → "on"
Owner (CODEOWNERS): @payments-team
Type:              Release toggle
Risk:              R1 (low)
```

**Generated PR:**

```
Title: chore(flags): remove new_checkout_v2 (100% on since 2025-02-14)

Summary
  Flag has served `on` to 100% of production for 84 days with zero
  toggle activity. Removing both the flag check and the dead v1
  checkout component.

Changes
  - src/checkout/route.tsx        : -28 +4
  - src/checkout/CheckoutV1.tsx    : deleted (-512)
  - src/checkout/CheckoutV1.css    : deleted (-180)
  - src/checkout/__tests__/...     : -1 file, -94 lines
  - src/analytics/checkout.ts      : -6 +1

Rollback Plan
  Revert this commit. v1 component preserved on branch
  archive/ff-new-checkout-v2 for 90 days. Re-enable flag in LD
  via the saved config in the linked ticket.

Service-side follow-up
  - Archive flag in LD on merge (Workflow scheduled)
  - Hard-delete flag 2026-08-01 (90 days post-merge)

Tickets
  PROJ-4421 (close on merge)
```

### Example 3: Custom DB Flag Audit

A team running a home-grown `feature_toggles` table:

```sql
-- Step 1: code-referenced keys (output of grep)
WITH code_refs(key) AS (VALUES
  ('multi_currency'), ('beta_dashboard'), ('legacy_pricing'),
  ('async_export'),  ('new_search_v2')
)
SELECT ft.key,
       ft.enabled,
       ft.updated_at,
       (SELECT 1 FROM code_refs c WHERE c.key = ft.key) AS in_code
FROM   feature_toggles ft
ORDER  BY ft.updated_at;
```

The agent emits the migration plus the code PR in one bundle:

```
PR-1 (DB migration M0142_drop_dead_toggles.sql)
  DELETE FROM feature_toggles
  WHERE key IN ('legacy_pricing', 'beta_dashboard', 'old_v1');

PR-2 (code)
  - drop legacy_price_engine.py
  - drop beta_dashboard route
  - prune calls in 4 files
```

PR-2 merges first; PR-1 deploys in the next migration window.

## Output

The agent produces:

- **Inventory CSV** — every flag with service, code-refs, telemetry, owner, type, risk, recommendation
- **Per-owner ticket queue** — Jira/Linear-ready with one ticket per flag, grouped by owner
- **Removal PRs** — actual diffs, batched by R-grade
- **Rollback plan** — per-PR rollback section + 30/60/90 calendar reminders
- **Cleanup dashboard** — flag count, removable count, $/yr savings estimate, weekly burndown
- **Provider-specific scripts** — API delete commands, archive commands, segment cleanup
- **Prevention pack** — PR template, CI lint, expiry-required policy, onboarding doc
- **Four-week sprint plan** — daily checklist, owners, definition of done

## Common Scenarios

### "We just acquired a company with 400 flags in a tool we don't use"
The agent maps each flag to one of: keep-and-migrate, remove-with-default, remove-as-dead-code. Migration target is your incumbent flag service. Output is two PR streams: code PRs (own repo) and import scripts (for the incumbent service).

### "An R2 removal caused a P1 incident"
The agent generates the immediate-revert PR and a postmortem template. Then it adds the missing detection: which staleness rule should have caught this, and patches the ruleset (e.g. add "no diurnal pattern in evaluations" as R17).

### "How much is flag debt actually costing?"
The agent estimates: vendor cost (MAU × $rate × removable_traffic_share), engineering time tax (avg 6 min per stale flag in PR review × refs/quarter), and incident risk (count of incidents in the last 12 months that mention a flag). One-page CFO-ready memo.

### "Our team owns 80 flags and the rest of the org owns 1,200 — should we wait?"
No. The agent ships the team's queue independently. Cross-team coordination kills cleanups. Each team should own its flag retirement budget.

## Tips for Best Results

- Provide both the service export and a code-references grep — single-source audits miss orphans
- Share 30+ days of evaluation telemetry, not a snapshot — variance reveals diurnal experiments
- Include CODEOWNERS or an equivalent ownership map — owner-less queues stall
- Specify which environments matter (prod only, or prod+staging) — staging-only flags often look stale but aren't
- State your incumbent flag service if doing a migration — it changes the migration target, not just the cleanup logic
- Mention regulatory constraints (PCI, HIPAA, GDPR) before starting — kill switches in those domains move from R4 to "do not touch"

## When NOT To Use

- **Brand-new product with <30 flags** — the audit overhead is larger than the debt; instead apply the prevention pack at flag #1.
- **Active migration between flag vendors** — finish the migration first; mid-migration audits produce false positives because both systems are partially live.
- **Code-base under active rewrite** — flags being removed by the rewrite anyway; wait until the rewrite ships, then audit what survived.
- **Compliance-driven flags only** (banking kill switches, regulatory toggles) — these are R4 by default; they require legal/compliance review, not engineering cleanup.
- **You don't have evaluation telemetry** — without last-evaluation data, the staleness rules collapse to "old" which produces too many false positives. Wire up telemetry first, audit second.
