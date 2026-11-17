## Description:

Use external AI assistants such as ChatGPT, Claude, Gemini, or DeepSeek when an agent needs help with complex problems, knowledge gaps, or deeper reasoning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoxu1232](https://clawhub.ai/user/xiaoxu1232)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent users use this skill to let an agent consult supported third-party AI assistants when a task is difficult, requires multi-round reasoning, or has an acknowledged knowledge gap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task details may be sent to third-party AI services, especially when Trust Mode is used.

Mitigation: Keep Ask Mode as the default and require user review of exactly what will be sent before any external AI request.

Risk: Private code, credentials, personal data, regulated data, or confidential business information could be exposed to outside AI services.

Mitigation: Do not use Trust Mode for sensitive work, and remove secrets or confidential content before consulting an external AI assistant.

## Reference(s):

- [ask-ai on ClawHub](https://clawhub.ai/xiaoxu1232/skills/ask-ai)
- [ChatGPT](https://chatgpt.com)
- [Claude](https://claude.ai)
- [Gemini](https://gemini.google.com)
- [DeepSeek](https://chat.deepseek.com)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Markdown or plain text summaries from external AI assistant consultation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external AI responses summarized back to the user; no structured output contract is specified.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
