## Description:

Send batch messages with delivery tracking to OpenClaw agents via Telegram or other channels, supporting scheduling, templating, and fallback routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheben77](https://clawhub.ai/user/cheben77)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators maintaining OpenClaw agent deployments use this skill to broadcast messages, trigger agent workflows, schedule heartbeat checks, and review delivery status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages are sent through local Telegram bot tokens to a built-in Telegram user ID.

Mitigation: Replace or remove the built-in recipient ID, require an explicit approved recipient, and run the skill only with Telegram tokens you control.

Risk: The heartbeat installer can create recurring Telegram sends through cron and write logs under /tmp.

Mitigation: Review the schedule, log path, and removal process before installing the cron heartbeat.

Risk: Message templates or triggered broadcasts could disclose sensitive operational data through Telegram.

Mitigation: Review messages and template variables before dispatch, and do not send secrets or private operational data.

## Reference(s):

- [Agent Messenger ClawHub page](https://clawhub.ai/cheben77/skills/agent-messenger)
- [cheben77 publisher profile](https://clawhub.ai/user/cheben77)
- [Telegram Bot API endpoint used by scripts](https://api.telegram.org/bot)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local scripts that read OpenClaw Telegram bot tokens, send Telegram messages, and optionally install a cron heartbeat.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
