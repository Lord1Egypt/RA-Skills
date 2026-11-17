## Description:

CSV Processor Pro helps data engineers and data governance teams clean large CSV files with streaming processing, YAML rules, schema validation, quality scoring, deduplication, export, and audit guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Data engineers, data integration teams, and data governance practitioners use this skill to guide CSV cleaning workflows for large files, custom rule configuration, schema checks, quality scoring, deduplication, exports, and audit logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags inconsistent API/network instructions and automatic network diagnostics that do not fit the stated local CSV-processing purpose.

Mitigation: Review the skill before restricted or production use, allow only expected local CSV-processing commands, and reject unrelated network diagnostics unless separately justified.

Risk: CSV cleaning and export workflows can alter datasets or create derivative files that may carry sensitive source data.

Mitigation: Use copied input data, write outputs to new files, and protect quality reports and audit logs with the same access controls as the source datasets.

Risk: The artifact contains conflicting statements about API-key use and licensing, which can lead to incorrect operational assumptions.

Mitigation: Do not provide API keys unless a specific trusted dependency requires them, and confirm the release license before publication or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/csv-processor-pro)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, YAML, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to create cleaned CSV data, Parquet/JSON/Excel exports, quality reports, and local audit logs when the described commands are executed.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
