## Description:

Validates data quality in pipelines by checking completeness, consistency, freshness, accuracy, schema drift, and distribution anomalies, then generates quality reports and expectations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and analytics teams use this skill to audit pipeline data, profile datasets, detect anomalies, define data quality expectations, and produce actionable quality reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Data quality audits may expose sensitive records, identifiers, secrets, customer data, or proprietary fields if raw datasets are provided unredacted.

Mitigation: Provide only the datasets and paths needed for the audit; redact or mask PII, secrets, tokens, customer identifiers, and proprietary fields where possible, and prefer aggregate summaries or safe sample fields in generated reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/data-quality-validator)
- [Publisher profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with inline code blocks, SQL or Python expectations, monitoring rules, scorecards, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include quality scores, dimension scores, critical issues, data profiles, schema drift findings, freshness dashboards, distribution analysis, trend analysis, and recommended next actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
