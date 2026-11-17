## Description:

Creates a new OpenAgent agent and binds it to a Telegram Bot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangzhiyu](https://clawhub.ai/user/liangzhiyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure a Telegram bot account, create an OpenClaw agent, bind the bot to that agent, restart the gateway, and verify the binding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram bot tokens can be exposed through shared terminals, shell history, logs, or permissive configuration files.

Mitigation: Use a staging token while testing, avoid pasting real tokens into shared logs, restrict configuration file permissions, and rotate any token that may have been exposed.

Risk: Binding an agent and restarting the gateway changes a live messaging integration.

Mitigation: Validate the agent binding and gateway restart in a staging environment before applying the same steps to production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liangzhiyu/skills/create-agent-telegram)
- [ClawHub publisher profile](https://clawhub.ai/user/liangzhiyu)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes placeholder values for bot name, bot token, and agent ID.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
