# find-community-help Project Notes

Use this file as the project-level handoff guide for future agents working in this repository.

## Product Boundary

`find-community-help` is a lightweight skill protocol package. It helps a host agent seek mature external experience when the active thread is stuck, progress has stalled, local attempts are repeating, the agent may be reinventing a known solution, or the user explicitly asks for community help.

Keep these boundaries intact:

- stdlib-only Python scripts
- no daemon, database, crawler, scheduler, or background service
- host-managed scheduling only
- semantic trigger gate before any advisory plan is considered useful
- heartbeat, scheduled, task-end, and idle fallback are delivery windows only
- default `search_mode = low`
- default `tool_preference = public-only`
- output remains `advisory_only: true`
- output remains `thread_scope: active_conversation_only`
- never write help hints into system prompts, persona files, permanent memory, or core agent instructions

Do not turn this skill into a broad search tool. Every change should improve a common rule, trigger class, contract field, or test category, not a single warning, page, or fixture.

## Workflow

Think in this order:

1. Skill behavior: `SKILL.md` and the relevant `references/*.md`
2. Trigger policy: `references/trigger-policy.md`
3. Query/source guidance: `references/search-playbook.md`
4. Suggestion contract and threat rules: `references/suggestion-contract.md` and `references/threat-model.md`
5. Optional mechanical checks: `scripts/should_travel.py`, `scripts/plan_travel.py`, and `scripts/validate_suggestions.py`
6. Reliability, ablation, real-trigger, and workflow smoke tests

Actual web or community search is performed by the host agent. This repo should not grow a real search engine, scraper, or script-based judge for whether community advice is good.

## Source Policy

Search engines are discovery tools, not evidence. Retained suggestions should cite original sources with `tier_source_kind` labels.

Prefer security advisories, official docs, release notes, changelogs, and maintainer-owned GitHub surfaces. Use ClawHub metadata as primary evidence only for skill distribution facts such as version, install surface, static scan state, and listing content. Treat ClawHub reviews, non-maintainer GitHub threads, Stack Overflow, maintained Q&A, and independent research papers as secondary validation. Blogs, forums, Reddit, social posts, and chat-community summaries stay tertiary.

## Public Documentation

Keep public surfaces aligned:

- `SKILL.md` is the ClawHub display surface.
- `README.md` is the GitHub English landing page.
- `README.zh.md` is the Chinese user-facing page.
- `agents/*.yaml` should use display name "Find Community Help" and prompt `$find-community-help`.

`agent-travel` is a legacy migration name only.

## Test Gate

Before publishing or claiming a fix, run:

```powershell
python -m py_compile scripts\should_travel.py scripts\plan_travel.py scripts\validate_suggestions.py scripts\reliability_test_suggestions.py scripts\ablation_test_suggestions.py scripts\community_smoke_test.py scripts\real_trigger_scenarios.py scripts\real_prompt_scenarios.py scripts\_report_utils.py scripts\_test_mutators.py
python scripts\should_travel.py examples\states\heartbeat-ready.json
python scripts\plan_travel.py examples\states\heartbeat-ready.json --context examples\thread-contexts\openclaw-cron-drift.txt
python scripts\validate_suggestions.py references\suggestion-contract.md
python scripts\real_trigger_scenarios.py
python scripts\real_prompt_scenarios.py
python scripts\reliability_test_suggestions.py
python scripts\ablation_test_suggestions.py
python scripts\community_smoke_test.py
git diff --check
```

Expected current shape:

- reliability: all cases pass, crash count is 0
- real trigger scenarios: all trigger-to-plan scenarios pass
- real prompt scenarios: all prompt-to-plan scenarios pass
- ablation: current guardrail rejection rate is 1.0 and safe acceptance is 1.0
- community smoke: trigger, validator, query-plan, and forbidden-leak checks pass; keyword scoring and hallucination deltas are report-only review aids

## Release Discipline

Before a GitHub or ClawHub publish, verify the working tree, run the full test gate, inspect ClawHub after publish, and confirm static scan/verdict state. Keep `.clawhubignore` focused on shrinking the publish package, not hiding required runtime files.
