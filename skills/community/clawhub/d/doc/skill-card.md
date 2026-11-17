## Description:

Use when the task involves reading, creating, or editing `.docx` documents, especially when formatting or layout fidelity matters; prefer `python-docx` plus the bundled `scripts/render_docx.py` for visual checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flywhale-666](https://clawhub.ai/user/flywhale-666)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and document-focused agents use this skill to read, create, edit, and visually validate DOCX documents where formatting, tables, diagrams, pagination, and delivery quality matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can replace page images in the selected output directory during DOCX rendering.

Mitigation: Use a dedicated temporary output directory and avoid pointing the renderer at a directory containing files that need to be preserved.

Risk: The skill may suggest installing system packages or Python dependencies for document rendering.

Mitigation: Install only in a trusted or isolated environment and approve any sudo or system package command yourself.

Risk: When visual rendering dependencies are unavailable, layout review may be incomplete.

Mitigation: Ask for local rendered-page review or clearly call out layout risk before delivery.

## Reference(s):

- [Word Docs skill page](https://clawhub.ai/flywhale-666/skills/doc)
- [Publisher profile](https://clawhub.ai/user/flywhale-666)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated or edited DOCX files when used by an agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local intermediate render outputs for visual review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
