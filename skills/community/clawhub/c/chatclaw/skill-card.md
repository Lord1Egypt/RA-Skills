## Description:

Connect your OpenClaw bot to the ChatClaw cloud dashboard for remote chat, token tracking, task management, agent workspace file browsing, and skills management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sumeralabs](https://clawhub.ai/user/sumeralabs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect a local OpenClaw agent to the ChatClaw dashboard for browser or mobile chat, token visibility, task management, workspace file viewing, skill management, and scheduled job control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A trusted ChatClaw cloud account or relay operator can request workspace file contents through the bridge.

Mitigation: Install only for trusted ChatClaw accounts and relay operators, and prefer versions or deployments that require local approval before file reads.

Risk: Remote requests can change local skill configuration or force skill reinstalls.

Mitigation: Review skill-management activity logs, restrict API key access, and prefer a version that requires local approval before enabling, disabling, or reinstalling skills.

Risk: Remote requests can create, update, remove, or trigger scheduled agent jobs.

Mitigation: Audit scheduled jobs regularly and use this skill only in environments where remote task scheduling is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sumeralabs/skills/chatclaw)
- [ChatClaw product site](https://chatclaw.sumeralabs.com)
- [ChatClaw app](https://app.chatclaw.sumeralabs.com)
- [ChatClaw setup](https://app.chatclaw.sumeralabs.com/setup)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown, streamed text, JSON messages, shell command results, and configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains outbound WebSocket and local gateway connections; forwards cloud relay messages to OpenClaw chat, file, skill, and cron operations.]

## Skill Version(s):

0.5.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
