## Description:

A Feishu-optimized OpenClaw scheduling skill that guides agents to create reliable one-time and recurring tasks with the `openclaw cron add` CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhc888007](https://clawhub.ai/user/jhc888007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to translate natural-language scheduling requests into correctly parameterized OpenClaw cron commands for Feishu private chats, Feishu group chats, multi-agent deployments, and terminal-triggered tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent scheduled tasks using shell-formatted commands with user-controlled message text.

Mitigation: Require the agent to show the exact schedule, recipient or channel, account, timezone, and structured command arguments before creating a task.

Risk: Incorrect Feishu routing or account selection can send scheduled messages to the wrong private chat, group chat, or agent account.

Mitigation: Confirm the `user_id` or `chat_id`, Feishu account, and single-agent or multi-agent mode before running the generated OpenClaw command.

Risk: The README suggests adding a persistent `TOOLS.md` routing rule for future scheduling requests.

Mitigation: Only add that persistent rule when the installer explicitly wants future scheduling requests routed to this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jhc888007/skills/cron-creator-feishu)
- [OpenClaw cron troubleshooting guide](https://mp.weixin.qq.com/s/iQtW-SKRcvngzbpJXMSSxg)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and CLI argument guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands include schedule, timezone, recipient/channel, account, isolated session, wake, stagger, and delete-after-run parameters where applicable.]

## Skill Version(s):

1.0.13 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
