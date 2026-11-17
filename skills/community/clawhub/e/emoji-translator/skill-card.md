## Description:

Translates Chinese or English text to emoji, explains emoji back as text, and supports smart inline emoji insertion, keyword search, category browsing, and meme-style additions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eelowl](https://clawhub.ai/user/eelowl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate short Chinese or English text into emoji-enhanced text, pure emoji, or plain-language emoji explanations for chat, captions, search, and lightweight content formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Python helper on user-provided text.

Mitigation: Installers should review the disclosed helper scripts and run the skill in the normal local execution boundary used for agent skills.

Risk: Broad trigger phrases may route casual emoji requests to this skill when precise routing matters.

Mitigation: Review and narrow trigger phrases during installation or orchestration if the host agent has multiple overlapping translation or formatting skills.

Risk: Keyword matching covers common emoji and may miss niche, newer, or long-sentence cases.

Mitigation: Treat generated emoji translations as lightweight suggestions and have the agent summarize or verify ambiguous outputs before user-facing use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eelowl/skills/emoji-translator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON from local Python commands, usually summarized in Markdown by the agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include inline emoji-enhanced text, pure emoji lists, emoji meanings, search results, or category listings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
