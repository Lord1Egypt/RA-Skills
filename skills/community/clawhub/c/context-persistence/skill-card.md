## Description:

Helps agents design file-based memory, progress tracking, and shared-state patterns that preserve context across isolated sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgy2020](https://clawhub.ai/user/lgy2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to design workspace-file memory systems for agents that run across main sessions, cron jobs, subagents, and heartbeats. It provides patterns for persistent notes, daily logs, task progress files, and shared state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent context files can retain secrets, sensitive personal data, or stale user details.

Mitigation: Review writes to MEMORY.md and memory/ files, avoid storing sensitive data unless necessary, and define retention or pruning practices.

Risk: Daily logs and progress files can grow without bound and become harder to review.

Mitigation: Use concise curated memory files, keep progress files scoped to one task, and apply practical size or retention limits.

Risk: Multiple sessions updating shared state can overwrite each other or create inconsistent progress.

Mitigation: Use append-only logs, include complete progress state at checkpoints, and add leases or atomic write practices where concurrent sessions are expected.

## Reference(s):

- [Cross-Session Context Sync](artifact/references/cross-session-sync.md)
- [Memory File Patterns](artifact/references/memory-patterns.md)
- [Progress Tracking for Long-Running Tasks](artifact/references/progress-tracking.md)
- [ClawHub Skill Page](https://clawhub.ai/lgy2020/skills/context-persistence)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with templates, checklists, and inline code or shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose workspace memory files, daily logs, progress files, and shared-state files; no API calls or credentials are required.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
