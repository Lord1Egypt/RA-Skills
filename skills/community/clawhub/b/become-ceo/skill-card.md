## Description:

Your AI executive team on Discord. 7 specialists (engineering, finance, marketing, devops, legal, management, chief of staff) each with its own model and personality. Use when setting up, configuring, scaling, or troubleshooting a multi-bot Discord workspace where you are the CEO and AI agents are your team.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanikua](https://clawhub.ai/user/wanikua)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to set up and operate a Discord-based executive team of specialized AI agents for engineering, finance, marketing, DevOps, legal, management, and coordination tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default Discord setup gives broad invocation access across configured bots.

Mitigation: Restrict bots to trusted guilds, channels, roles, and users before deployment.

Risk: The installation flow uses an unpinned global npm package install.

Mitigation: Pin and review the clawdbot package version before installing or upgrading it.

Risk: Discord and LLM credentials are required for operation.

Mitigation: Protect tokens, scope them narrowly where possible, and rotate them if exposed.

Risk: Finance, legal, DevOps, and engineering agents may be granted sensitive authority in a workspace.

Mitigation: Avoid attaching powerful tools until authorization, review, and audit controls are in place.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wanikua/skills/become-ceo)
- [AGENTS.md - Workspace Rules](references/AGENTS.md)
- [IDENTITY.md - Team Structure](references/IDENTITY.md)
- [SOUL.md - Team Rules](references/SOUL.md)
- [USER.md - About You](references/USER.md)
- [clawdbot-template.json](references/clawdbot-template.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires clawdbot, LLM provider credentials, Discord bot tokens, and a local clawdbot configuration file.]

## Skill Version(s):

1.5.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
