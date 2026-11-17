## Description:

Generates styled, multi-sheet Excel reports from XLSX, CSV, or JSON data using industry templates, formulas, charts, KPI dashboards, and column mapping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moniq888](https://clawhub.ai/user/moniq888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operations teams can use this skill to generate professional Excel reporting workbooks for manufacturing, retail, finance, internet, medical, and general KPI workflows. It is suited to converting trusted business data into styled dashboards, detail sheets, formulas, and charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Template or report paths can trigger unsafe code or spreadsheet formula execution.

Mitigation: Review or patch formula handling before installation, use only trusted templates and trusted source data, and apply spreadsheet formula protections before opening generated workbooks.

Risk: Generated reports may be automatically opened after creation.

Mitigation: Disable or patch auto-open behavior before processing untrusted data or producing workbooks in sensitive environments.

Risk: Attacker-influenced output paths may affect where generated files are written.

Mitigation: Constrain output directories and avoid user-controlled output paths unless they are validated by the calling workflow.

Risk: The documentation mentions email flags and SMTP credentials, but server security guidance says the inspected CLI does not implement documented email sending.

Mitigation: Do not provide SMTP credentials to this skill unless email behavior is reviewed, implemented, and tested in the release being used.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/moniq888/skills/excel-report)
- [Artifact Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Excel workbooks (.xlsx) with Markdown and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated workbooks may contain spreadsheet formulas, charts, styled sheets, and template-driven filenames.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
