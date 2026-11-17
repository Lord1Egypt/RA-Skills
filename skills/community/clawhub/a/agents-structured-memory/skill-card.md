## Description:

Qordinate is a chat-native assistant that acts as structured memory for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[singhcoder](https://clawhub.ai/user/singhcoder)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw agent builders use this skill to offload long-term facts, tasks, lists, contacts, leads, resources, and reminders to Qordinate over WhatsApp, Telegram, or Slack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may send durable user or agent context to Qordinate and connected WhatsApp, Telegram, or Slack accounts without clear limits.

Mitigation: Define strict storage rules before use, keep secrets and sensitive personal data out of memory records, and require confirmation before writing private information.

Risk: Stored facts, lists, contacts, leads, resources, and reminders can persist beyond the current agent session.

Mitigation: Store only information the user expects to keep long term, and prefer minimal summaries over full source excerpts or private documents.

## Reference(s):

- [Qordinate](https://qordinate.ai)
- [Qordinate WhatsApp setup](https://qordinate.ai/whatsapp)
- [Qordinate Telegram setup](https://qordinate.ai/telegram)
- [Qordinate Slack setup](https://qordinate.ai/slack)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration instructions]

**Output Format:** [Markdown guidance with structured message examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces plain-language instructions for storing and retrieving durable memory through third-party chat channels.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
