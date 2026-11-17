## Description:

Complete A-Z Discord server administration. Channel/role/member management, AutoMod, webhooks, templates, audit logs, scheduled events, threads, and full server control via CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thebigbrainchad](https://clawhub.ai/user/thebigbrainchad)

### License/Terms of Use:


## Use Case:

Developers, Discord server operators, and moderation teams use this skill to generate and run CLI workflows for managing Discord channels, roles, members, AutoMod, webhooks, audit logs, scheduled events, threads, and bulk moderation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make powerful live Discord server changes with broad bot authority.

Mitigation: Use a least-privilege Discord bot instead of ADMINISTRATOR, scope permissions to the intended guild, and review each destructive command before execution.

Risk: Credential handling is weak if bot tokens are passed through command lines or exposed in logs.

Mitigation: Keep Discord bot tokens in environment variables or a secret manager, avoid putting tokens in shell history, and rotate any token that may have been exposed.

Risk: Bulk moderation and webhook-management commands can cause large-scale or hard-to-audit server changes.

Mitigation: Avoid bulk moderation or webhook commands until safeguards and redaction are added, or run them only after dry-run review in a controlled maintenance window.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thebigbrainchad/skills/discord-admin)
- [Discord API v10](https://discord.com/api/v10)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, configuration examples, and JSON-oriented CLI usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included shell scripts call the Discord API and may emit JSON responses, status messages, or errors depending on the command.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
