# Trigger Policy

Use this file when `find-community-help` needs to decide whether the agent should seek outside help.

## Semantic Trigger Matrix

At least one semantic signal must be present. Delivery windows alone are never enough.

| Signal | State field | Use when | Default mode |
| --- | --- | --- | --- |
| No clear next step | `no_clear_next_step` or legacy `unresolved_blocker_count >= 1` | Local inspection has not produced a plausible next action. | `low` |
| Progress stalled | `progress_stalled` or legacy `user_corrections >= 2` | The task is not moving despite reasonable local work. | `medium` |
| Repeated local attempts | `repeated_local_attempts >= 2`, `attempted_fixes_count >= 2`, or legacy `related_failures >= 2` | The agent is looping over the same failure or fix path. | `medium` |
| Reinventing-wheel risk | `suspected_reinventing_wheel` | A maintained library, official recipe, known issue, or community pattern may already exist. | `low` |
| User-requested community help | `user_requested_community_help` or legacy `user_explicit_search_request` | The user asks for community experience, known bugs, mature approaches, or outside examples. | `medium` |
| User-requested deep help | `user_requested_deep_community_help` or legacy `user_explicit_deep_research_request` | The user asks for a broader external pass. | `high` |
| Version mismatch | `version_mismatch_seen` | Current docs or package behavior may differ from the model's memory. | `low` |

## Description-Level Reading

Read the skill description as an agent-facing boundary, then map it to the semantic matrix:

- "Blocked agent work" means the active thread has a concrete unresolved task, not a curiosity lookup.
- "Active task is stalled" maps to `progress_stalled` or a clear no-progress narrative from the user or agent.
- "Looping" maps to repeated local attempts, repeated corrections, related failures, or the same fingerprint returning.
- "Version-sensitive" maps to docs, releases, registry metadata, package behavior, or model memory that may be stale.
- "Likely covered by known issues/libraries" maps to reinventing-wheel risk, maintained recipes, known issues, or mature community patterns.
- "User asks for official/community guidance" maps to explicit user request; manual requests still need redaction, source scoping, and advisory-only output.
- "Dry-run only; no browsing or durable memory" is an output boundary: build a plan or hint, then let the host/user decide whether to search.

## Delivery Windows

These values describe how a host invokes the skill; they do not trigger the skill by themselves.

- `user_request` or `manual_request`: explicit user request; skip quiet timing gates, still redact and scope the search.
- `failure_recovery`: automatic recovery path; requires a semantic signal.
- `task_end`: task-end retrospective; requires a semantic signal.
- `heartbeat`: host background wakeup; requires a semantic signal and quiet gates.
- `scheduled`: host-managed or user-configured periodic check; requires scheduled ownership, neutral host-generated prompts, and a semantic signal.
- `idle_fallback`: only when heartbeat is unavailable or explicitly enabled; requires a semantic signal.

## Automatic Safety Gates

For all automatic delivery windows, run only when all of these are true:

- no user operation in progress
- no agent response in progress
- no tool approval pending
- active conversation within `24h`
- run limits have not been reached

Default limits:

- `active_conversation_window = 24h`
- `quiet_after_user_action = 20m`
- `quiet_after_agent_action = 5m`
- `repeat_fingerprint_cooldown = 12h`
- `max_runs_per_thread_per_day = 1`
- `max_runs_per_user_per_day = 3`

Repeated runs with the same fingerprint should stay quiet until the cooldown elapses. Bypass the cooldown only when the user explicitly asks for help, the host sets `semantic_escalation_since_last_hint: true`, or `last_travel_semantic_signals` shows that a new semantic signal appeared since the previous hint.

## Scheduled Prompt Policy

For `scheduled` triggers, distinguish manual prompts from host-generated prompts:

- A host-managed scheduled run is valid only when the host states ownership explicitly.
- A user-configured periodic run is valid only when the user opted in.
- Manual scheduled prompts may preserve the operator's wording.
- Host-generated scheduled prompts must stay neutral and workflow-derived from logs, backlog items, docs drift, or other task facts.
