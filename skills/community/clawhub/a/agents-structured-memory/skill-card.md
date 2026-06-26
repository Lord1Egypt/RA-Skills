## Description: <br>
Qordinate gives OpenClaw agents durable chat-native memory for long-term facts, tasks, lists, and reminders over WhatsApp, Telegram, or Slack. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SinghCoder](https://clawhub.ai/user/SinghCoder) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and OpenClaw agent builders use this skill to offload selected facts, tasks, contacts, leads, resources, and reminders into Qordinate rather than maintaining a custom database. The user must connect a Qordinate account to WhatsApp, Telegram, or Slack before an agent can send or retrieve memory through that channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected facts, tasks, contacts, leads, resources, and reminders may be stored in Qordinate through WhatsApp, Telegram, or Slack. <br>
Mitigation: Set clear user-approved rules for what the agent may save, and avoid secrets, credentials, tokens, health or financial details, and private internal material. <br>
Risk: The skill depends on the user's connected Qordinate account and chosen chat platform. <br>
Mitigation: Confirm the account and channel are connected before relying on Qordinate as durable agent memory. <br>
Risk: Incorrect or overly broad memory writes can persist stale or unwanted information. <br>
Mitigation: Have the agent include explicit list names and structured fields, and review important writes or updates before sending them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/SinghCoder/agents-structured-memory) <br>
- [Qordinate](https://qordinate.ai) <br>
- [Qordinate WhatsApp Setup](https://qordinate.ai/whatsapp) <br>
- [Qordinate Telegram Setup](https://qordinate.ai/telegram) <br>
- [Qordinate Slack Setup](https://qordinate.ai/slack) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance and natural-language structured text messages for chat platforms] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the user to connect a Qordinate account to WhatsApp, Telegram, or Slack before agent use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
