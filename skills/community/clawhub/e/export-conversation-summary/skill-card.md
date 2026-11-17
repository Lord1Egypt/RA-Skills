## Description:

Export current Claude Code conversation to markdown document with full dialogue context and model operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youngbeauty](https://clawhub.ai/user/youngbeauty)

### License/Terms of Use:


## Use Case:

Developers and Claude Code users use this skill to create a durable markdown transcript of a problem-solving session, including dialogue, summarized tool activity, conversation statistics, and evaluation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save sensitive conversation history and detailed tool activity into a persistent markdown file without redaction.

Mitigation: Review and redact the generated markdown before sharing, committing, or storing it outside the local workspace.

Risk: Conversation exports may contain secrets, internal paths, command output, proprietary code, private project details, or personal information.

Mitigation: Use a limited or redacted export when the conversation involved credentials, proprietary debugging, or other sensitive material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youngbeauty/skills/export-conversation-summary)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown transcript with summarized tool activity, conversation statistics, and evaluation sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a persistent conversation export, usually under docs/{YYYY-MM-DD}-conversation.md, and reports the output path, line count, and file size.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
