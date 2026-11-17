## Description:

书本学习助手 helps learners study books from either verified online book information or user-provided ebook files, producing structured chapter overviews, core ideas, thinking tools, accessible examples, and timeliness checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhanchao883](https://clawhub.ai/user/wangzhanchao883)

### License/Terms of Use:

MIT-0

## Use Case:

External learners, educators, and reading assistants use this skill to turn a book title or local ebook into structured study notes, then drill into selected chapters with examples and current-knowledge checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated notes may be written to Notion, Obsidian, or synced note locations without clear confirmation.

Mitigation: Confirm the destination and obtain approval before allowing any write action to synced notes.

Risk: Local ebook parsing can expose the agent to untrusted or very large ebook files.

Mitigation: Process only trusted ebooks, keep size limits in place, and stop if parsing behavior is unexpected.

Risk: PDF support depends on an optional parser dependency.

Mitigation: Install the PDF dependency only when needed, pin the version, and use a constrained environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangzhanchao883/skills/book-learning-assistant)
- [Ebook local reading guide](artifact/EBOOK_README.md)
- [Output examples](artifact/references/output-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured Markdown, with JSON returned by the ebook helper script when invoked]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include chapter lists, extracted text snippets, examples, and timeliness assessments; ebook helper output can be truncated with a limit parameter.]

## Skill Version(s):

1.5.0 (source: server release metadata; SKILL.md frontmatter lists 1.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
