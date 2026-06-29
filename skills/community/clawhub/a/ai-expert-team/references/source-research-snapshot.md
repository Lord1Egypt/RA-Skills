# Source Research Snapshot

Use this as the condensed research basis for the first `ai-expert-team` implementation. It preserves the session-specific detail without bloating `SKILL.md`.

## Claude Code Findings

- Agent definitions should be treated as structured routing data, not just prose.
- Tool boundaries, required MCP servers, and availability checks should be explicit before dispatch.
- Verification agents should combine real execution output with a parseable verdict.
- A later definition can override an earlier same-name agent type in agent lists, so names should be unique and collision-aware.

## Agency Agents Findings

- The useful pattern is a searchable specialist catalog, not full prompt preload.
- Divisions and role metadata are governance aids; specialist prompts still need task-specific scope, acceptance criteria, and tool boundaries.
- NEXUS-style handoffs are valuable because they preserve from/to/task/evidence context between agents.
- Reality Checker and Evidence Collector are first-class roles, not optional polish.
- The catalog can inspire specialist selection, but its role bodies should not be copied blindly into final prompts.

## Nuwa Skill Findings

- CEO archetypes should be compact structured profiles, not pure persona voice.
- Useful profile fields include trigger domains, decision lens, challenge style, honest boundaries, forbidden domains, and research-before-answer rules.
- The strongest examples include fallback rules, anti-patterns, and quality gates.
- Specialist personas such as `x-mastery-mentor` should not be mixed into the general CEO pool.

## Design Corrections Captured

- The supported design is Single-CEO Expert Team, not a multi-CEO board.
- `ai-expert-team` is the public skill name; `Single-CEO Expert Council` is the internal architecture pattern.
- Expansion ideas were intentionally removed; improve the current single-CEO workflow before adding new modes.
- Validation evidence is required before claiming the workflow is fully proven.
- Read-only requests must not leak edit / stage / commit / push steps into handoffs.
- More agents is not automatically better; prefer 3-5 specialists with non-overlapping deliverables.
