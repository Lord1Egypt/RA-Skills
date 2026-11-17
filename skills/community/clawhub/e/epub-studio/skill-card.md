## Description:

Epub Studio helps agents create professional EPUB ebooks from Markdown, text, or structured content with chapters, table of contents, cover images, and metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, authors, and content teams use this skill to guide agents in generating EPUB ebooks from Markdown or structured text, including chapters, table of contents, cover images, and metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency behavior can change if ebooklib is installed without a reviewed version.

Mitigation: Install the dependency in a virtual environment and pin ebooklib to a reviewed version before use.

Risk: Generated EPUB files could be written to unintended locations if the output path is not chosen carefully.

Mitigation: Generate files only to explicit, user-selected output paths.

Risk: Untrusted Markdown or HTML content may carry unsafe markup into generated ebook content.

Mitigation: Sanitize untrusted Markdown or HTML before conversion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobewin/skills/epub-studio)
- [ClawHub publisher profile](https://clawhub.ai/user/tobewin)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python code snippets; generated EPUB files when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and the ebooklib Python package; writes EPUB output to user-selected file paths.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
