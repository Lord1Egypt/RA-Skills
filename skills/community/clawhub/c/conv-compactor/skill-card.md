## Description:

A multilevel conversation compaction skill that monitors context length and condenses conversation history into structured summaries while preserving key information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sinnzen](https://clawhub.ai/user/sinnzen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to compact long conversations before the context window is exhausted, preserving user decisions, technical details, errors, fixes, current work, and next steps for continued work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may summarize a conversation when the user did not intend to compact context.

Mitigation: Prefer explicit invocation and confirm that compaction is desired before replacing active conversation context.

Risk: A generated summary can omit details needed for ongoing work.

Mitigation: Review the summary for missing decisions, files, errors, fixes, current work, and next steps before relying on it.

Risk: Conversation history can include secrets or local identifiers.

Mitigation: Apply the skill's redaction rules for API keys, tokens, passwords, secrets, credentials, and full local paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sinnzen/skills/conv-compactor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries should redact secrets and avoid copying every user message verbatim.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
