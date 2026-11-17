## Description:

Review electrical schematics from EPLAN and similar CAD tools against standardized checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Electrical engineers and automation reviewers use this skill to inspect schematic PDFs and review templates for safety, main circuit, control circuit, PLC/IO, servo, and communication-network issues before release or retrofit sign-off.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Python package behavior may vary if dependencies are installed without version control.

Mitigation: Use a virtual environment and pin PyMuPDF, openpyxl, and reportlab versions before operational use.

Risk: The skill references a checklist file that is not included in the artifact.

Mitigation: Verify or provide the review checklist before using generated findings for design decisions.

Risk: Generated PDF report labels are Chinese-language by default.

Mitigation: Adapt the report script or request translated report text when the review audience needs another language.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/electrical-schematic-review)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with checklist findings and optional Excel or PDF report-generation instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce localized report labels and expects user-verified review criteria.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
