## Description:

Summarize and format markdown files, then apply mkdocs/material-compatible structural spacing fixes for math, list, and table blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smilingwayne](https://clawhub.ai/user/smilingwayne)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and documentation maintainers use this skill to improve Markdown readability, create analysis and formatted copies, and apply MkDocs Material-compatible spacing fixes before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated formatting, title, summary, or metadata changes could alter how readers interpret a document.

Mitigation: Review the analysis report and formatted Markdown before relying on or publishing the output.

Risk: Structural-fixes-only mode can modify the original Markdown file in place.

Mitigation: Use the formatted-copy workflow for important documents and reserve in-place fixes for intentional edits.

Risk: The skill uses npm-based formatting support, so local dependency installation may be required before running the script.

Mitigation: Install dependencies from the provided lockfile and run the formatter in a controlled workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/smilingwayne/skills/format-markdown)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, analysis reports, shell commands, and completion summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write formatted copies, modify Markdown spacing in place, and create backups when overwriting existing output files.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
