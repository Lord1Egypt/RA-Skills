## Description:

Cleans, validates, and standardizes clinical trial data for CDISC SDTM-oriented regulatory workflows, including missing-value handling, outlier detection, date standardization, and audit-trail reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical data managers, clinical programmers, and regulatory submission teams use this skill to prepare DM, LB, and VS datasets for SDTM-style cleaning and review. It supports conservative data preparation workflows that preserve traceability through generated cleaning reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinical trial data may include sensitive information, and the security evidence flags privacy-scope gaps.

Mitigation: Use approved non-sensitive test data unless the execution environment has appropriate privacy controls for real trial data.

Risk: Cleaning operations can affect data integrity if generated outputs are mistaken for source records.

Mitigation: Preserve original datasets separately and choose output paths that cannot overwrite raw data.

Risk: Generated SDTM-oriented outputs and reports may not be sufficient for regulatory reliance on their own.

Mitigation: Independently validate SDTM compliance and review cleaning reports before relying on the generated outputs.

## Reference(s):

- [SDTM Implementation Guide Reference](references/sdtm_ig_guide.md)
- [Domain Specifications](references/domain_specs.json)
- [Outlier Thresholds](references/outlier_thresholds.json)
- [Common Patterns](references/common-patterns.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files, json]

**Output Format:** [Markdown guidance with Python and shell examples; CSV or Excel cleaned datasets and JSON cleaning reports when the packaged script is executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports CSV and Excel inputs, configurable missing-value and outlier strategies, and generated audit-trail reports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
