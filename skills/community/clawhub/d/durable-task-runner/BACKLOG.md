# BACKLOG.md

Status legend: `todo` | `doing` | `blocked` | `done`

## Verified complete

- [done] Bootstrap project artifacts so the runner can manage its own build
- [done] Add configurable defaults and reporting/memory thresholds
- [done] Keep explicit attribution/provenance for borrowed concepts
- [done] Add timed status reporting every 5 minutes regardless of milestone, optimized for minimal-token / maximum-information output (progress-bar style if practical)
- [done] Add heartbeat/progress helper with reporting levels
- [done] Extend task reporter to show both current task progress and full project status as separate progress bars
- [done] Add subagent dispatch/controller helper
- [done] Tighten dropped-line checks and worker-result handling without bloating the controller
- [done] Connect thin controller helper to real subagent runs
- [done] Add resume bootstrap helper for running tasks after reset
- [done] Add bootstrap-driven resume recommendations for concrete controller actions
- [done] Add controller-ready resume plans from bootstrap output
- [done] Add low-risk controller resume-apply path from bootstrap output
- [done] Validate resume/apply flow on a non-bootstrap durable task
- [done] Add repeatable smoke script for validation task creation/bootstrap/apply
- [done] Define task complexity levels (0..N) and artifact-selection rules
- [done] Add STATUS.md format and live project status updates
- [done] Add DECISIONS.md for architectural/process choices
- [done] Add memory reference file and MEMORY.md pointer rule

## Remaining work

- [done] Add tests or more repeatable smoke coverage for core helpers where real usage shows value
- [done] Dogfood the runner on a separate real-world long task
- [done] Make the repo GitHub-ready and clearly installable as a skill package

## Notes

This file is intentionally editable mid-flow.
New work discovered during execution can be added here without pretending the original plan was complete.

## Release hardening follow-through

- [done] Tighten the public skill body for ClawHub-style consumption
- [done] Add a concrete quickstart reference for repeated use
- [done] Add a deterministic clean-bundle export path for publishing
- [done] Verify the clean publish bundle in isolation, not just from the dev repo
- [done] Add explicit license/provenance/runtime notes for public preview readiness

## Post-0.1.0 / 0.1.1 candidate

- [done] Add explicit safe delivery modes (`stdout`, `noop`, `log-only`) alongside live OpenClaw delivery
- [done] Add targeted delivery-path smoke coverage, including immediate-send behavior and no-binding/no-loop checks
- [done] Add a concrete scheduler/setup helper for recurring `task_tick_all.py` operation

## Deferred beyond 0.1.1

- [todo] Harden unattended continuation so once a durable project starts it keeps moving to completion by default unless the user pauses/stops/edits it or a real blocker is recorded; durability must mean continuation, not just resumability
- [todo] Add hot-context compaction guardrails: when active durable work reaches roughly 45% session context, checkpoint durable state and prepare clean handoff; at 50% hard stop, automatically pause the project, record state durably, initiate a session reset, and resume/continue the project immediately from durable state when the new session comes up
- [done] Add a lightweight release checklist so each release consistently updates status/docs, verifies the publish bundle, and tags/publishes from a known-good state
- [done] Keep a concise release history / changelog so post-0.1.x changes are understandable without spelunking commit logs
- [done] Refresh release/status docs as part of each release so `STATUS.md` and publish-facing notes do not drift behind actual tagged versions
- [done] Trim development-only smoke scripts out of the ClawHub publish bundle while keeping them in the source repo
- [done] Add explicit security / operational notes in public docs so ClawHub reviewers do not have to infer core behavior from the code alone
- [todo] Auto-bind new durable tasks in the active chat/session so progress delivery works without manual delivery-binding setup
- [todo] Make recurring tick execution ambient by default in suitable environments instead of requiring the operator to remember cron/timer setup
- [todo] Add a richer real-world example project/reference walkthrough for new adopters
- [todo] Expand reporting-mode docs and operator guidance once real usage shows which knobs are actually confusing
- [todo] Continue README/public-facing copy cleanup so the first lines stay optimized for ClawHub/search while remaining honest about methodology, release posture, and what belongs to the dev repo versus the publish bundle
- [todo] Add a strict config reference doc for `config/defaults.json`, including valid values, ranges, defaults, and invalid-value behavior
- [todo] Add a config validator for `config/defaults.json` that checks shape, types, enums, and numeric ranges with useful path-based errors
- [todo] Add a safe defaults recovery path: if the active defaults file is missing, repopulate it from stock known-good defaults instead of failing awkwardly
- [todo] Add a quick reset/revert helper for defaults, with both stock-reset behavior and an optional user-preferred baseline that does not overwrite the canonical stock fallback
- [todo] Reassess progress-bar math after more real-world use and tighten the metric so it stays grounded in explicit state rather than vague operator feel
- [todo] Consider weighted milestones / better roll-up rules only if that improves signal without turning reporting into workflow theater
- [todo] Add optional per-project/per-task config overrides for higher-complexity work when global defaults become too blunt
- [todo] Consider broader controller/subagent ergonomics only after more real-world use justifies the extra surface area
