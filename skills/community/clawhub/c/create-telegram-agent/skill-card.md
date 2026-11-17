## Description:

Creates a new Telegram agent in OpenClaw by collecting an agent name, purpose, and bot token, preparing configuration, and requiring confirmation before modifying openclaw.json.

This skill is ready for commercial/non-commercial use.

## Publisher:

[4t-shirt](https://clawhub.ai/user/4t-shirt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to set up a Telegram-backed agent workspace, prepare OpenClaw configuration entries, and generate initial AGENTS.md and SOUL.md files after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose a Telegram bot token by asking the agent to show the full token in chat.

Mitigation: Mask bot tokens in previews and summaries, prefer a secret mechanism when OpenClaw supports one, and revoke or regenerate any token exposed in chat logs or screenshots.

Risk: The skill modifies OpenClaw configuration and creates local agent files after confirmation.

Mitigation: Review the proposed configuration before approving changes and verify the generated workspace, binding, and Telegram account entries before restarting the gateway.

## Reference(s):

- [CreateTelegramClawAgent on ClawHub](https://clawhub.ai/4t-shirt/skills/create-telegram-agent)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with JSON snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces proposed OpenClaw configuration, user-review prompts, directory creation commands, and initial agent files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
