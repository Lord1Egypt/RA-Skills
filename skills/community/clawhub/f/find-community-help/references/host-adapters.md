# Host Adapters

Use this file when a host needs a minimal adapter policy for `find-community-help`.

## Shared Rule

- Treat `find-community-help` as an advisory help-retrieval skill for stuck active threads.
- Require at least one semantic trigger: no clear next step, stalled progress, repeated local attempts, suspected reinventing wheel, or explicit user request.
- Treat heartbeat, scheduled, task-end, and idle fallback as delivery windows only.
- Keep search tools `public-only` by default.
- Read the isolated suggestion channel only when the next task matches the fingerprint and TTL.

## Markdown-First Boundary

- Treat `SKILL.md` and `references/*.md` as the source of truth for agent behavior.
- A human or agent can use this skill by reading only the Markdown files and writing a compact advisory plan.
- Use `scripts/should_travel.py` only to simulate host-state gates for automatic delivery windows.
- Use `scripts/plan_travel.py` only to preview a redacted query plan; the agent still reads the Markdown before searching.
- Use `scripts/validate_suggestions.py` only for mechanical suggestion-block structure, not for judging the quality of community advice.
- Keep redaction in scripts because accidental secret echo is a safety and output-hygiene problem, not a reasoning preference.
- Keep `scripts/*test*.py` and `scripts/real_trigger_scenarios.py` as release verification harnesses.
- Treat community output as advisory until the user authorizes any execution or code change. For repo, package, skill, plugin, or registry suggestions, surface available GitHub/ClawHub/SkillHub safety status before applying the suggestion.

## Script Audit

Current scripts should remain optional helpers, not prompt authorities:

| Script | Current role | Keep only when | Do not use it for |
| --- | --- | --- | --- |
| `should_travel.py` | Host-state dry-run for automatic delivery windows, quiet windows, cooldowns, and rate limits | A host adapter needs deterministic scheduling safety checks | Deciding that community help is useful when the Markdown semantic trigger is absent |
| `plan_travel.py` | Redacted query-plan preview with `dry_run: true` and `network_used: false` | The host may turn thread context into search text and needs mechanical redaction | Replacing source reading, judging advice quality, or expanding the search scope |
| `validate_suggestions.py` | Suggestion-block structure, source-tier shape, TTL, and advisory-only checks | Release checks, CI, or hosts that require a stable interchange format | Deciding whether a community idea is correct or mature |
| `community_smoke_test.py` | Real workflow fixture smoke | Release verification | Runtime behavior |
| `real_trigger_scenarios.py` | Trigger-to-plan regression and description coverage | Release verification before publishing | Runtime behavior |
| `real_prompt_scenarios.py` | Prompt-to-plan regression for realistic user wording | Release verification before publishing | Runtime behavior |
| `reliability_test_suggestions.py` and `ablation_test_suggestions.py` | Baseline, regression, and ablation checks | Release verification and rollback decisions | Runtime behavior |

0-script use is feasible for manual agent operation: read `SKILL.md`, `trigger-policy.md`, `search-playbook.md`, `suggestion-contract.md`, and `threat-model.md`, then produce an advisory plan in Markdown. 0-script host automation is feasible only if the host already provides equivalent redaction, quiet-window, rate-limit, and structural validation elsewhere. Until then, keep scripts as adapters and tests, not as the source of behavioral constraints.

## OpenClaw

- Prefer heartbeat, task-end, failure-recovery, scheduled, or explicit user windows only after the semantic gate is true.
- Keep background execution redacted, quiet, rate-limited, and free of pending tool approvals.
- Do not let heartbeat or cron alone become the reason to seek help.

## Hermes

- Treat `find-community-help` as a progressive-disclosure skill.
- Do not load large reference files unless the skill is invoked.
- Prefer small-scope help retrieval by default.
- Keep all stored hints advisory-only.

## OpenAI / Codex-style hosts

- Keep manual invocation available for operators who want a one-off community-help pass.
- Keep automatic model invocation disabled unless the host has an explicit safety wrapper around the delivery window.
- Prefer the same `public-only`, advisory-only, next-relevant-turn flow used by the other adapters.
