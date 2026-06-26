# Changelog

## v0.1.5

Release focus:
- fix timed status/reporting behavior after immediate updates in live durable runs
- centralize status snapshot rendering so ticker/send layers share one source of truth
- keep cron-helper interval handling explicit and less confusing for publish users

Expected notes:
- timed reporting now respects a bounded cooldown after immediate sends instead of getting stuck behind stale gating
- status delivery records the rendered snapshot payload alongside the sent line for easier diagnosis
- ticker rendering now consumes the shared status snapshot helper instead of duplicating progress math
- cron helper now takes `INTERVAL_SEC` and validates whole-minute cron-compatible values

## v0.1.4

Release focus:
- make the ClawHub bundle smaller, clearer, and easier to trust at a glance
- re-center the product on reset-safe durable recovery instead of scheduler theater
- remove development-only smoke scripts from the public bundle
- add explicit security / operational notes to public docs
- keep the source repo useful for development while making the published skill more reviewable

Expected notes:
- smoke-test scripts remain in the source repo but are excluded from the publish bundle
- public docs explain plaintext task state, delivery modes, and subagent control surface more directly
- new `task_continue.py` provides the primary user-facing **"continue this"** recovery path after interruption/reset
- bootstrap can now prefer asking whether to resume interrupted work instead of blindly continuing
- public bundle now includes `task_continue.py`
- ClawHub-facing package is more intentional about what end users actually need to install/use
- stale ordinary `running` tasks are now pause-cleaned instead of looping forever with fake continuation heartbeats
- tick sweeps avoid sending misleading recurring bars for tasks just reclassified out of the active lane
- added `task_context_guard.py` to make the 45% prepare / 50% hard-stop-reset-resume policy scriptable instead of just aspirational

## v0.1.2

Release focus:
- refresh release hygiene and project status so docs match the real repo state
- carry forward the post-0.1.1 candidate work already completed in the repo
- make the next publish/tag step honest and easier to reason about

Expected notes:
- explicit release-discipline backlog follow-through
- refreshed `STATUS.md` for current version reality
- concise release-history tracking so users do not need to infer version meaning from commit logs alone

## v0.1.1

- publication-pass improvements after the initial public preview lane
- safer / clearer publish-readiness and packaging follow-through
- scheduler/setup helper and delivery-path hardening for recurring reporting flow
- safe delivery modes (`stdout`, `noop`, `log-only`) and related smoke coverage

## v0.1.0

- first public preview / initial publishable release posture
- durable task state model, task control helper, progress reporting, resume bootstrap, and packaging baseline
