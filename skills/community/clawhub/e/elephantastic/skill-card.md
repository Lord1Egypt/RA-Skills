## Description:

Executive function stack for AI agents: GTD-style task management, error/learning capture, and periodic self-review using Taskwarrior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lux-sp4rk](https://clawhub.ai/user/lux-sp4rk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Elephantastic to give autonomous agents a local task-management and review workflow for preserving focus, capturing errors and learnings, and resuming work across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release may appear to be only a deprecation or rename notice, but evidence shows it includes active workflows and scripts that can change local state.

Mitigation: Review the package before installing and use it only when a local executive-function system with Taskwarrior, heartbeat checks, and persistent-memory workflows is intended.

Risk: Task deletion, heartbeat cron setup, and edits to persistent agent memory files can affect agent behavior or local records.

Mitigation: Require explicit approval before task deletion, cron setup, or edits to AGENTS.md, SOUL.md, TOOLS.md, identity files, or equivalent memory files.

## Reference(s):

- [Taskwarrior](https://taskwarrior.org)
- [Taskwarrior Schema Reference](references/taskwarrior-schema.md)
- [Periodic Review Runbook](references/review-runbook.md)
- [Vitality Heartbeat](references/vitality-heartbeat.md)
- [Sovereign Agent Executive Stack](references/executive-stack.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and bundled Python and Bash scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local Taskwarrior changes, heartbeat checks, and session handoff summaries when its scripts or workflows are executed.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
