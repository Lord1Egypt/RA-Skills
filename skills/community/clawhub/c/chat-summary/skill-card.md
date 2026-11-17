## Description:

Chat Summary organizes chat records and conversation histories into topic-clustered, structured summaries with multilingual support for Chinese, English, Traditional Chinese, Japanese, and Korean.

This skill is ready for commercial/non-commercial use.

## Publisher:

[garyyinclaw](https://clawhub.ai/user/garyyinclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and knowledge workers use this skill to summarize selected chat sessions into topic-based daily summaries, meeting notes, long-conversation digests, and archives. It can produce local Markdown or plain text output and optionally prepare Notion page content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected chat history may contain sensitive or private information.

Mitigation: Use explicit session limits, avoid sensitive or private conversations, and follow the skill's guidance to omit sensitive content.

Risk: Optional Notion or translation integrations can send summary text to external services.

Mitigation: Enable Notion or translation providers only when external processing is intended and use the relevant API keys deliberately.

Risk: Summaries may omit context or overstate conclusions from the original conversation.

Mitigation: Preserve original conclusions, cite important message sources where available, and review summaries before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/garyyinclaw/skills/chat-summary)
- [Topic clustering rules](references/clustering-rules.md)
- [Notion API usage guide](references/notion-api.md)
- [Translation integration guide](references/translation.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Structured Markdown, plain text, or Notion page content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports topic limits, summary length targets, language selection, and optional Notion export.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
