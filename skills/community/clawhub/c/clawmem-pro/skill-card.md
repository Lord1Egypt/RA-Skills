## Description:

ClawMem Pro installs a file-based persistent memory system for OpenClaw sessions, including MEMORY.md, daily notes, cron inbox, heartbeat routines, and optional scheduled extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marc69-69](https://clawhub.ai/user/marc69-69)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add durable workspace memory to OpenClaw sessions, seed operator context, and maintain daily notes that can be promoted into long-term memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory files may contain sensitive operator, project, or personal context.

Mitigation: Install only in a private, trusted workspace and do not store secrets, tokens, regulated data, or confidential third-party information in memory files.

Risk: Recurring cron or Windows scheduled tasks can run memory extraction and heartbeat behavior in the background.

Mitigation: Enable scheduling only after reviewing the scripts and schedule; on Windows, avoid Administrator setup unless least-privilege behavior has been confirmed.

Risk: Cron inbox entries from other sessions, jobs, or sub-agents may be promoted into long-term memory.

Mitigation: Treat inbox entries as untrusted notes and review MEMORY.md before future sessions rely on promoted content.

## Reference(s):

- [ClawMem Pro on ClawHub](https://clawhub.ai/marc69-69/skills/clawmem-pro)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown guidance with inline shell and PowerShell commands, plus generated workspace files from bundled templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and maintains local memory files; optional cron or scheduled-task setup can run recurring background jobs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
