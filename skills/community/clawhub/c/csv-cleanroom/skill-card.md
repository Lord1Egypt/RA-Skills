## Description:

Profile messy CSV files, standardize columns, detect data quality issues, and produce a reproducible cleanup plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operations teams use this skill to profile messy CSV data, normalize schemas, identify data quality issues, and draft reproducible cleanup plans before applying changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive CSV data that the user provides.

Mitigation: Use it only with files intentionally shared for the task, avoid sensitive datasets unless intended, and review generated JSON before acting on it.

Risk: Cleanup plans or generated outputs could lead to destructive data changes if applied without review.

Mitigation: Prefer preview, draft, or simulation mode first and document irreversible operations before applying them.

## Reference(s):

- [CSV Cleanroom on ClawHub](https://clawhub.ai/52yuanchangxing/skills/csv-cleanroom)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)
- [Data Quality Checklist](resources/data_quality_checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON profile output from the bundled Python script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include a profile report, normalized schema, cleanup plan, quality scorecard, remediation checklist, and preview-first recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
