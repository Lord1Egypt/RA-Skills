## Description:

Automates recruiting new agents, configuring dedicated Feishu or Discord bots, and rebuilding multi-account routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[htf0513](https://clawhub.ai/user/htf0513)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw operators and developers use this skill to create HR-style agent workspaces, bind each agent to a dedicated Feishu bot, and optionally configure Discord bot routing for team operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify OpenClaw configuration and restart the gateway.

Mitigation: Use it only in a test or tightly controlled OpenClaw environment, manually back up ~/.openclaw before use, and review configuration changes before applying them to production.

Risk: The skill may handle Feishu App Secrets or Discord Bot Tokens during bot binding.

Mitigation: Do not paste real secrets or bot tokens into chat; provide credentials through controlled environment variables or a reviewed local process.

Risk: Open direct-message routing and persistent agent authority can broaden bot access.

Mitigation: Restrict bot senders before enabling routing and avoid production binding until unsafe shell calls, plaintext secret storage, open-DM defaults, and confirmation gaps are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/htf0513/skills/feishu-team-manager)
- [Skill documentation](artifact/SKILL.md)
- [Quick start](artifact/QUICK_START.md)
- [Discord setup guide](artifact/promotion/DISCORD_SETUP_GUIDE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, generated files, and JSON configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the OpenClaw CLI, local OpenClaw configuration access, Feishu credentials, and optional Discord bot credentials.]

## Skill Version(s):

2.4.3 (source: server release metadata and changelog, released 2026-04-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
