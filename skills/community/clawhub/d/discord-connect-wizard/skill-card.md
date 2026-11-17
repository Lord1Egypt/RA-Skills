## Description:

Discord Connect Wizard helps an OpenClaw agent onboard a Discord bot on one local machine, including bot setup, intents, guild invite, OpenClaw configuration, gateway restart, and DM pairing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gm4leejun-stack](https://clawhub.ai/user/gm4leejun-stack)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to connect a new Discord bot while minimizing manual work to Discord-controlled login, CAPTCHA, MFA, OAuth authorization, and DM steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a Discord bot token during setup.

Mitigation: Use a secure local input path where possible, avoid pasting tokens into chat, and rotate the token if it was exposed.

Risk: The skill changes local OpenClaw Discord configuration and restarts the gateway.

Mitigation: Review the intended OpenClaw environment before installation and run the wizard only on the machine whose configuration should be changed.

Risk: A colliding OpenClaw Discord account ID may be overwritten.

Mitigation: Review existing OpenClaw Discord accounts before running the setup and confirm that the target account ID is new.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gm4leejun-stack/skills/discord-connect-wizard)
- [Conversation mode](references/conversation-mode.md)
- [OpenClaw Discord baseline](references/openclaw-discord-baseline.md)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Discord API v10](https://discord.com/api/v10)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, browser-action prompts, and local wizard instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local OpenClaw configuration changes, gateway restart, and Discord pairing approval.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
