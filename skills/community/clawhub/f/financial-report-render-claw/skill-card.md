## Description:

Turns financial and operating analysis results into polished report files with structured sections, charts, and export paths for HTML, PDF, Word, Markdown, and PNG outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external report preparers, and developers use this skill to turn existing financial, operating, or project analysis into formal report configurations, charts, and rendered report files for review or presentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted report text or image paths can be written into generated HTML or PDF output and can trigger arbitrary resource loads.

Mitigation: Use trusted report JSON and local chart assets, sanitize report text and image paths before rendering, and review rendered output before sharing.

Risk: Advertised PPT and dashboard capabilities are not substantiated by the reviewed artifact behavior.

Mitigation: Plan around the supported HTML, PDF, DOCX, Markdown, and PNG chart workflow unless PPT or dashboard support is added and reviewed.

## Reference(s):

- [Report Configuration Specification](references/report-config-spec.md)
- [Report Templates](references/report-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/tujinsama/skills/financial-report-render-claw)
- [Publisher Profile](https://clawhub.ai/user/tujinsama)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON report configuration, shell commands, and generated report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports HTML, PDF through WeasyPrint or browser print flow, DOCX through python-docx, and PNG chart generation from CSV inputs.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
