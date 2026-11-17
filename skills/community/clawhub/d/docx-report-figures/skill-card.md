## Description:

Adds source-grounded tables and matplotlib figures to existing Chinese or English research reports in DOCX while preserving report text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wang-shuanglin](https://clawhub.ai/user/wang-shuanglin)

### License/Terms of Use:

MIT-0

## Use Case:

Research writers and analysts use the skill to add traceable tables and data figures to an existing Chinese or English report while preserving its body text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF export may close all accessible Word sessions, including sessions with unsaved work.

Mitigation: Save documents and close other Word sessions before running the PDF export; use a disposable environment when practical.

Risk: Layout verification removes existing p*.png files in its pages directory.

Mitigation: Use a dedicated empty pages directory or back up matching PNG files before running verification.

Risk: The security scan is partial because one local path-like reference could not be resolved.

Mitigation: Review the unresolved reference and complete a security scan before installation.

## Reference(s):

- [ClawHub release](https://clawhub.ai/wang-shuanglin/skills/docx-report-figures)
- [Plan schema](artifact/references/plan-schema.md)
- [Scientific report style guide](artifact/references/sci-report-style.md)

## Skill Output:

**Output Type(s):** [DOCX reports, PDF previews, PNG figures, Tables, Data visualizations]

**Output Format:** [An edited DOCX report with inserted tables and figures, plus a PDF preview and PNG figure files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exhibit values are traceable to source passages; report body text is preserved.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
