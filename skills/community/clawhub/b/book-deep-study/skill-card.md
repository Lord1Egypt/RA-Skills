## Description:

Book Deep Study guides agents to help users study books, PDFs, long articles, or learning materials through chapter-by-chapter, dialog-based deep reading, while this deprecated release redirects to an external canonical skill path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanjinlimkelvin-dot](https://clawhub.ai/user/tanjinlimkelvin-dot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn reading material into a staged study dialogue that emphasizes chapter structure, core claims, key arguments, and understanding checks. Because this release is deprecated and redirects to an external canonical skill path, review that target before relying on the behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deprecated entry point redirects the agent to an absolute filesystem path outside the reviewed package.

Mitigation: Install or use this release only after reviewing and trusting the canonical skill at that path.

Risk: The reviewed package may not contain the behavior users expect from the public skill summary.

Mitigation: Treat this package as a deprecated pointer and validate the canonical skill before depending on its study workflow.

## Reference(s):

- [Chapter-by-Chapter Book Deep Study Prompt](references/chapter-by-chapter.md)
- [Patterns for Book Deep Study](references/patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/tanjinlimkelvin-dot/skills/book-deep-study)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown study guidance with structured sections and questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are conversational and chapter-scoped; the deprecated package points to a canonical skill outside the reviewed artifact.]

## Skill Version(s):

3.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
