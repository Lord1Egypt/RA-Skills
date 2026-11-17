## Description:

Converts PPT, PPTX, and PDF files into a presentation package with per-slide images and narration scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianglingling007](https://clawhub.ai/user/jianglingling007)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and presenters use this skill to prepare slide-deck or PDF narration packages before playback in Claw Body or review as text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup workflow installs presentation and PDF processing dependencies, including system packages where supported.

Mitigation: Review the setup script before execution and install dependencies in a trusted local environment.

Risk: The skill writes slide images, extracted text, speaker notes, and narration scripts into the workspace, which may expose confidential deck content.

Mitigation: Use trusted storage for confidential presentations, review generated files, and remove sensitive outputs when they are no longer needed.

Risk: Unpinned dependencies can change behavior across installations.

Mitigation: Pin package versions before setup when reproducibility or deployment controls are required.

## Reference(s):

- [Claw Presenter on ClawHub](https://clawhub.ai/jianglingling007/skills/claw-presenter)
- [LibreOffice Download](https://www.libreoffice.org/download/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus generated presentation.json and PNG slide files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a workspace presentation folder containing extracted slide metadata, speaker notes where available, generated narration text, and per-slide images.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
