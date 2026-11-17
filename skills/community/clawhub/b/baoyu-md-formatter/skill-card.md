## Description:

Formats plain text and Markdown into structured, reader-friendly Markdown with frontmatter, titles, summaries, headings, lists, tables, code formatting, and optional CJK typography fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and content maintainers use this skill to analyze and format plain-text or Markdown files into cleaner Markdown while preserving the original content. It can add frontmatter, titles, summaries, headings, lists, tables, code formatting, and typography cleanup for CJK and English mixed text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify Markdown or plain-text files, including in-place edits during typography-only workflows.

Mitigation: Keep backups before in-place runs and review formatted output before replacing important documents.

Risk: Generated titles, summaries, and frontmatter may be inaccurate or unsuitable for publication.

Mitigation: Review generated metadata and reader-facing text before publishing or distributing formatted documents.

Risk: Optional local command-line typography steps depend on the available runtime and local scripts.

Mitigation: Run only in trusted workspaces and confirm the local runtime command before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/baoyu-md-formatter)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files, Markdown analysis notes, frontmatter metadata, shell command suggestions, and concise completion reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create analysis and formatted Markdown files, may edit a source file in place for typography-only workflows, and may use local EXTEND.md preferences when present.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
