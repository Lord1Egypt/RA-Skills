## Description:

Automatically extracts key points from long Chinese or English text and returns concise bullet-point summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1466561686](https://clawhub.ai/user/1466561686)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents use this skill to summarize long messages, emails, meeting notes, articles, and chat transcripts into clear key points and action items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long messages may be sent to the configured LLM provider for summarization, including messages that exceed the length trigger without an explicit summary request.

Mitigation: Use this skill only where automatic summarization is desired, and avoid submitting confidential, regulated, or private text unless the configured LLM provider is approved for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1466561686/skills/cs)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style bullet-point summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the configured LLM provider with temperature 0.3 and a maximum response length of 1000 tokens.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
