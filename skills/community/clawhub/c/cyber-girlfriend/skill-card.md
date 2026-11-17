## Description:

Build or customize an owner-only proactive companion system with a cyber-girlfriend persona, Markdown private-life context, lightweight relationship memory, and OpenClaw presence cron delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kasanuowa](https://clawhub.ai/user/kasanuowa)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to set up or customize an owner-only proactive companion that sends scheduled private-life messages through OpenClaw. It helps generate local persona and schedule files, configure recurring delivery, preserve lightweight relationship memory, and validate the installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring companion delivery can use local messaging credentials and send owner-facing text or media automatically.

Mitigation: Review the skill before enabling it, require explicit confirmation before creating or enabling cron jobs, and keep delivery credentials in local configuration or environment variables.

Risk: Custom WeChat endpoints and automatic media recovery may expose credential or transcript-access risks.

Mitigation: Do not enable custom WeChat endpoints or automatic media delivery unless strict allowlists and dispatch-scoped files are in place.

Risk: The skill creates local relationship and state files that may contain personal context.

Mitigation: Keep generated persona, schedule, state, and life-log files local, owner-only, and excluded from published defaults.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kasanuowa/skills/cyber-girlfriend)
- [Standard Init / Upgrade Flow](artifact/references/standard-init-upgrade-flow.md)
- [Configuration](artifact/references/configuration.md)
- [Turn Contract](artifact/references/contract-schema.md)
- [First-Time Setup Guide](artifact/references/first-time-setup.md)
- [Presence Integration](artifact/references/presence-integration.md)
- [Private Life Layer](artifact/references/private-life-layer.md)
- [Required Events And Cron](artifact/references/required-events-and-cron.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration, local file edits, and shell command proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces owner-facing companion setup guidance and local runtime artifacts; recurring delivery and media behavior require review before enabling.]

## Skill Version(s):

2.2.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
