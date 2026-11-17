## Description:

Cleans and standardizes clinical trial datasets with SDTM-oriented validation, missing value handling, outlier detection, date standardization, and audit reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renhaosu2024](https://clawhub.ai/user/renhaosu2024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, clinical data managers, and data engineers use this skill to prepare clinical trial CSV or Excel datasets for SDTM-aligned validation, cleaning, outlier review, date normalization, and audit trail generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can alter sensitive clinical trial spreadsheets and write cleaned datasets.

Mitigation: Run it only on copies in an isolated workspace, preserve raw source files, avoid overwriting inputs, and review generated audit reports before use.

Risk: Generated CSV or Excel outputs may be unsafe when opened in spreadsheet software if formula-like cell values are present.

Mitigation: Neutralize spreadsheet formulas before sharing or opening outputs, or treat generated spreadsheet files as potentially unsafe.

Risk: Python dependencies are unpinned.

Mitigation: Pin and review numpy, pandas, and scipy versions before installation or deployment.

Risk: Missing-value imputation and outlier handling can change clinical interpretation.

Mitigation: Have a qualified data manager or statistician review cleaning parameters and favor flagging outliers over removal for regulated workflows.

## Reference(s):

- [CDISC SDTM Implementation Guide Reference](references/sdtm_ig_guide.md)
- [Domain Specifications](references/domain_specs.json)
- [Clinical Outlier Thresholds](references/outlier_thresholds.json)
- [Common Clinical Data Cleaning Patterns](references/common-patterns.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/renhaosu2024/skills/clinical-data-cleaner)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python and bash snippets; generated CSV or Excel datasets and JSON audit reports when executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can alter clinical trial data outputs; preserve raw inputs and review generated audit reports before relying on results.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
