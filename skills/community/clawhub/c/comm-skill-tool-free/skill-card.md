## Description:

沟通助手基础版 helps an agent draft empathetic, context-aware communication using conversation history, emotional cues, communication templates, and tone or channel settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to draft replies for difficult conversations, customer emails, and other communication scenarios where tone, relationship, channel, and emotional context matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad file, shell, API, credential-checking, and callback behavior that is not clearly scoped to message drafting.

Mitigation: Grant only the tools needed for drafting, and require explicit approval before file access, shell commands, callbacks, external API calls, or credential checks.

Risk: Conversation inputs may contain sensitive personal, customer, or business context.

Mitigation: Review and redact sensitive content before sharing it with external services or saving generated drafts.

Risk: Generated drafts may misread emotional context or create communication that is inappropriate for a sensitive situation.

Mitigation: Have a human review drafts before sending, especially for high-stakes, legal, HR, customer, or conflict-related communication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/comm-skill-tool-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Communication drafts, structured guidance, and optional JSON, text, or CSV status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include execution status, metadata, and operation logs when structured output is requested.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
