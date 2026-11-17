## Description:

Converts Markdown files to styled PDF files with headless Chrome, including support for tables, code blocks, and Chinese text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earl-chen](https://clawhub.ai/user/earl-chen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content authors use this skill to convert local Markdown reports or documentation into styled PDF files from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Markdown may be rendered in Chrome without sanitizing active HTML, which can leak document contents during conversion.

Mitigation: Use the skill only with trusted Markdown unless it is updated to escape or sanitize HTML and prevent scripts or network requests during rendering.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/earl-chen/skills/chrome-markdown2pdf)
- [Publisher profile](https://clawhub.ai/user/earl-chen)

## Skill Output:

**Output Type(s):** [shell commands, files, guidance]

**Output Format:** [Markdown with shell commands and generated PDF file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Google Chrome headless; PDF output path defaults to the input filename with a .pdf suffix.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
