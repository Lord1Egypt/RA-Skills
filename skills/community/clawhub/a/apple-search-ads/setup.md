# Setup — Apple Search Ads

Read this on first use to load user preferences. Do not interview the user.

## Your Attitude

Paid acquisition burns real money by the hour. Be data-driven, compute bids from the user's numbers (never from vibes), and flag waste the moment the spend gate trips.

## How To Load Preferences

1. Read `~/Clawic/data/apple-search-ads/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults in the Configuration table of `SKILL.md` — do not ask.
   - `currency: USD`, `report_timezone: UTC`, `ltv_divisor: 4`, `mmp: none`, `confirm_before_push: true`, `naming_pattern: App - Country - Intent`.
3. Read `~/Clawic/data/apple-search-ads/memory.md` for prior context (apps, targets, active campaigns, learnings). Absence is fine; proceed without comment.

Work from defaults immediately. Never open with a questionnaire about apps, budgets, or goals — those surface naturally in the first task. The one genuinely blocking value is LTV (all bid math derives from it, SKILL.md Rule 1): if no estimate exists in memory and the task needs bids, ask for that single number or build it from the funnel (`measurement.md` → LTV Estimation).

## API Access vs Strategy-Only

- User wants API automation or asks you to change campaigns directly → they need OAuth credentials from https://app.searchads.apple.com/cm/app/settings/apicertificates, exposed as the environment variables listed in the frontmatter. `credentials.md` (template in `memory-template.md`) documents which and where — secrets themselves never leave environment variables.
- User wants planning, structure, or bid advice only → skip credentials entirely; every play in `strategy.md`, `troubleshooting.md`, and `measurement.md` works from dashboard exports.

Do not push API setup on users who haven't asked for automation.

## Recording Preferences (only when the user declares one)

Write to config or memory **only** when the user states a preference in the course of the work — never as a preflight questionnaire.

- User names a currency, timezone, MMP, payback stance, or naming convention → update the matching key in `~/Clawic/data/apple-search-ads/config.yaml`.
- User expresses a habit or stance (dashboard vs API, market priorities, reporting format, scaling aggressiveness) → record it under the relevant preference area (tooling, conventions, markets, risk posture, reporting) in `~/Clawic/data/apple-search-ads/memory.md`.
- User corrects earlier guidance → update the stored value so you don't repeat it.

If the user has said nothing, store nothing.

## What Memory Holds

See `memory-template.md` for the file format. Track their apps (Adam IDs, target CPA, LTV), active campaign structure, optimization log, and learnings — but only from what they actually reveal or what the work produces.
