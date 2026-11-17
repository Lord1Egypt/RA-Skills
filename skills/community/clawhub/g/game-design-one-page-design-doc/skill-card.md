## Description:

Create a concise one-page game design document and export it as both markdown and PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

Game designers, developers, and product teams use this skill to turn compact or messy game concept notes into a one-page design document suitable for quick review, pitching, and production alignment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency versions may affect PDF rendering reproducibility.

Mitigation: Install dependencies in a virtual environment and pin ReportLab when reproducible output matters.

Risk: The renderer writes output files and may overwrite files with the same names.

Mitigation: Review output paths before running the renderer.

## Reference(s):

- [Source Notes](references/source-notes.md)
- [Family Conventions](references/family-conventions.md)
- [Example Input](references/example-input.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured JSON, Markdown, and PDF files with concise implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The renderer writes requested JSON, Markdown, and PDF files and may overwrite same-named outputs.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
