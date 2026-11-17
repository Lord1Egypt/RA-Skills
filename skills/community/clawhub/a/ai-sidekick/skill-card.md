## Description:

Ai Sidekick helps OpenClaw agents configure persona files, user profiles, long-term memory practices, safety checks, skill management workflows, scheduled tasks, and token-saving behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bbroot](https://clawhub.ai/user/bbroot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to personalize an agent's behavior, memory, safety routines, workflows, and skill-management habits for ongoing workspace assistance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to persist user and operational memory across sessions.

Mitigation: Require explicit approval before writing USER.md, MEMORY.md, SOUL.md, logs, cron tasks, or backups.

Risk: Persistent memory may include credential paths or sensitive operational details.

Mitigation: Avoid storing credential paths or sensitive operational details in memory files.

Risk: Memory backups may expose retained user or workspace context.

Mitigation: Review backup permissions and use encryption where appropriate.

## Reference(s):

- [Server-resolved source repository](https://github.com/bbroot/ai-sidekick)
- [ClawHub skill page](https://clawhub.ai/bbroot/skills/ai-sidekick)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent changes to local behavior, memory, logs, cron tasks, and backup files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
