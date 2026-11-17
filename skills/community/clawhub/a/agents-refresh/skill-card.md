## Description:

Automatically refreshes agent context by reloading core identity and memory files, maintaining HEARTBEAT.md, and scheduling MEMORY.md distillation for long-running sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kentaroid-bot](https://clawhub.ai/user/kentaroid-bot)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to maintain continuity in long sessions by periodically rereading core context files and distilling recent logs into MEMORY.md.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring refresh jobs can repeatedly read identity, user, heartbeat, and historical memory files.

Mitigation: Review the cron and HEARTBEAT.md steps before enabling automation, and limit file access to the documented memory-maintenance paths.

Risk: Automated memory maintenance can rewrite long-lived MEMORY.md content.

Mitigation: Back up existing memory files and prefer a manual or review-before-write workflow unless ongoing scheduled updates are intentional.

## Reference(s):

- [Examples](references/examples.md)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/skills)
- [ClawHub Skill Page](https://clawhub.ai/kentaroid-bot/skills/agents-refresh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with cron JSON and file-edit examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scheduled memory-refresh guidance that reads core context files and updates MEMORY.md or HEARTBEAT.md.]

## Skill Version(s):

1.1.1 (source: server release metadata and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
