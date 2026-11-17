## Description:

Data visualization chart generator for creating bar, line, pie, scatter, and radar charts from data for reports, presentations, and documents, with PNG and SVG output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and document authors use this skill to turn CSV, Excel, JSON, manual, or extracted data into report-ready charts and embeddable chart outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill declares unpinned Python package installation.

Mitigation: Install it only in an isolated environment where accepting current package versions is appropriate.

Risk: Generated HTML or Markdown can include user-provided chart titles, captions, or width values.

Mitigation: Escape or validate these values before treating generated HTML or Markdown as trusted output.

Risk: The documentation overstates language support and mentions web data while the security summary characterizes the skill as local-only.

Mitigation: Confirm input source, language, and output requirements before relying on generated charts in production materials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobewin/skills/chart-maker)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks; generated chart files such as PNG, SVG, PDF, DOCX, XLSX, HTML, and Markdown when executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and Python packages including matplotlib, pandas, openpyxl, python-docx, and pillow; chart generation and file processing are described as local-only.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
