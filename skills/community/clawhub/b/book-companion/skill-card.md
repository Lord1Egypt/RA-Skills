## Description:

书搭子 is a privacy-focused local reading companion that helps users discuss books, maintain reading notes, and receive emotion-aware reading support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-innopower](https://clawhub.ai/user/ai-innopower)

### License/Terms of Use:

MIT-0

## Use Case:

Readers and developers use this agent to create a local reading profile, track books and reflections in Markdown, and receive personalized discussion or emotional support based on locally stored notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext local storage can expose reading history, emotional notes, private code words, dates, and user preferences.

Mitigation: Treat the data directory as sensitive, avoid storing unnecessary secrets, and use local disk or folder encryption when confidentiality is required.

Risk: Optional voice output can execute a user-provided TTS command even though the manifest reports external scripts and networking as disabled.

Mitigation: Enable voice output only after reviewing the exact TTS command and understanding any local execution or network behavior of the selected TTS tool.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-innopower/skills/book-companion)
- [书搭子知识库](artifact/references/knowledge_base.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and conversational text with optional shell command snippets and local Markdown file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores reading history, emotional notes, code words, and important dates as plaintext local Markdown files.]

## Skill Version(s):

2.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
