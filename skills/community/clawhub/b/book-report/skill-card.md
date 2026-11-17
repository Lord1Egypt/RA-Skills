## Description:

Book Report helps an agent generate structured book research deliverables, including an HTML study report and a Markdown conversation note kit from a book title, optional author, language mode, or text PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alzero-t](https://clawhub.ai/user/alzero-t)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research books for self-study or conversation, especially Chinese and English literary works. It organizes summaries, themes, characters, relationships, awards, author context, and quotes into reusable report artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted book titles can cause report files to be written outside the intended reports folder.

Mitigation: Sanitize report filenames and enforce directory-containment checks before writing generated files.

Risk: Private PDFs may be processed and persisted in generated report artifacts.

Mitigation: Use only PDFs the user is comfortable processing, and run the skill in an isolated environment when handling sensitive content.

Risk: Network-sourced book data can be incomplete or unavailable, which may reduce report accuracy.

Mitigation: Review generated reports before use and keep uncertainty labels for information that was not source-confirmed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alzero-t/skills/book-report)
- [Publisher Profile](https://clawhub.ai/user/alzero-t)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [HTML report files, Markdown note kits, shell commands, and generated file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports are written as files; optional PDF input is limited to text-based PDFs.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
