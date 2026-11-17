## Description:

Capture reading notes through conversation, organize by book, generate summaries, track reading list. Never lose an insight from a book again.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to capture conversational reading notes, quotes, summaries, reading-list state, and basic reading statistics organized by book.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes and reads local note, quote, metadata, and reading-list files.

Mitigation: Use a dedicated notes directory or configure booksDir explicitly so the skill does not mix with unrelated local files.

Risk: Local reading notes could be lost or corrupted through software bugs, system failures, or user error.

Mitigation: Keep independent backups of important reading notes and metadata.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/book-notes)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown and local JSON or Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local book note files, quote files, metadata, reading-list state, and reading statistics.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
