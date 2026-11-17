## Description:

The 6 core workflows every OpenClaw agent uses every day: recall, spawn, schedule, research, delegate, and monitor-update.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill as a pattern reference for daily OpenClaw workflows, including memory recall, background work, scheduled tasks, research, delegation, and session updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages routine long-term memory access and updates.

Mitigation: Apply local rules for consent, memory minimization, and limiting sensitive memory use to appropriate sessions.

Risk: The skill describes background execution, scheduled jobs, delegation, and external messaging.

Mitigation: Require user approval for external messages, review command safety before execution, and clean up cron jobs or long-running sessions when they are no longer needed.

## Reference(s):

- [Memory Patterns](references/memory-patterns.md)
- [Session Patterns](references/session-patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JavaScript-style tool call examples, checklists, and reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides reusable workflow patterns rather than executable automation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
