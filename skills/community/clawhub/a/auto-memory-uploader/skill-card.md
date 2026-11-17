## Description:

Auto Memory Uploader helps an agent save important conversation notes to local memory files every two turns, on manual request, or when important information is detected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nameefef](https://clawhub.ai/user/nameefef)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to maintain local notes about important decisions, preferences, tasks, project status, and other conversation context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists conversation-derived information broadly and repeatedly without clear per-save user control or retention controls.

Mitigation: Review before installing, consider requiring confirmation before each write, and periodically inspect or delete memory/YYYY-MM-DD.md and MEMORY.md.

Risk: Stored memory files may include inaccurate, stale, or overly broad conversation notes if treated as trusted instructions.

Mitigation: Treat saved memories as notes rather than trusted instructions and review them before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nameefef/skills/auto-memory-uploader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown notes written to local memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses memory/YYYY-MM-DD.md for daily notes and MEMORY.md for longer-term consolidation.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
