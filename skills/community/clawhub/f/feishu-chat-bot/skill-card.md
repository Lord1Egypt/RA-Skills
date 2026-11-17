## Description:

Feishu Chat Bot helps an agent automate Feishu group messages, reminders, approval notifications, team broadcasts, auto-replies, polls, and rich message cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[young-joey](https://clawhub.ai/user/young-joey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and team administrators use this skill to set up Feishu group-chat automations such as scheduled reminders, keyword replies, polls, status cards, and workflow notifications. It is intended for authorized Feishu groups where recipients and message content are explicitly reviewed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send, schedule, and broadcast messages to Feishu groups without clearly documented confirmation, recipient scoping, or cancellation controls.

Mitigation: Use only where the Feishu bot is authorized, recipients are explicit, message content is reviewed before sending, and scheduled or conditional automations can be disabled or audited.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/young-joey/skills/feishu-chat-bot)
- [Card template reference](artifact/references/card-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with message copy, JSON card examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Feishu message content, scheduled automation plans, rich-card JSON, poll structures, and recipient-scoping guidance.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
