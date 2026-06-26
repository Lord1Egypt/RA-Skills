# Find Community Help

Slug: `find-community-help`

Former name: `agent-travel`

GitHub: `gongyu0918-debug/find-community-help`

Version: `0.3.5`

License: MIT

Chinese notes: [README.zh.md](README.zh.md)

## What It Does

`find-community-help` prepares an outside-help lookup for a blocked thread.

It:

- decides whether outside help is justified
- creates a redacted dry-run query plan
- routes lookup toward official sources first, then community cross-checks
- validates the advisory hint contract before hints are stored

It does not browse, run commands from pages, write memory, or change core instructions.

## Trigger Conditions

Use this skill only when at least one condition is present:

- No clear next step after local inspection.
- Progress has stalled while the task is still active.
- The same failure, correction, or fix path keeps repeating.
- The task may already have an official pattern, maintained library, known issue, or community workaround.
- Docs, package behavior, registry metadata, or model memory may be stale.
- The user asks to find community experience, known bugs, mature solutions, official guidance, or outside examples.

`heartbeat`, `scheduled`, `task_end`, and `idle_fallback` are delivery windows only. They do not trigger the skill by themselves. Automatic runs still require redaction, quiet-window checks, rate limits, no pending tool approval, and no active user operation.

Do not use this skill for general browsing, news, pricing, broad research, or a simple one-shot error before local checks have run. Private or internal sources require explicit user opt-in.

## Routing

- Trigger decision: [references/trigger-policy.md](references/trigger-policy.md)
- Query plan and source order: [references/search-playbook.md](references/search-playbook.md)
- Hint format and validation: [references/suggestion-contract.md](references/suggestion-contract.md)
- Host integration: [references/host-adapters.md](references/host-adapters.md)
- Source trust and prompt-injection handling: [references/threat-model.md](references/threat-model.md)
- Test and fixture updates: [references/community-workflows.md](references/community-workflows.md)

## Output

The query plan is dry-run only:

- `community_help_plan: true`
- `dry_run: true`
- `network_used: false`
- one official or maintainer-owned anchor query
- optional community cross-check queries
- a redacted `host|version|symptom|constraint_pattern|desired_next_outcome` problem fingerprint

When browsing, scripts, file writes, or durable memory are not allowed, stop at this chat-visible plan. Do not emit a stored suggestion block until sources have actually been read.

Stored hints must remain:

- `advisory_only: true`
- `thread_scope: active_conversation_only`
- backed by at least one primary source and one independent non-primary source

Legacy `agent-travel` markers are accepted during migration. New integrations should use `find-community-help` markers.
