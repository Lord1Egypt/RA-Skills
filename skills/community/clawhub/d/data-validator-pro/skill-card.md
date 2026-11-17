## Description:

Data quality validation and profiling toolkit for tabular data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to profile tabular datasets, validate schemas, check completeness and constraints, and flag statistical anomalies before downstream analysis or pipeline use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency ranges for pandas and numpy can make audited deployments less reproducible.

Mitigation: Pin pandas and numpy versions in production or audited environments.

Risk: Arbitrary regex validation schemas from untrusted users can cause excessive validation runtime.

Mitigation: Accept schemas only from trusted users or enforce regex timeouts and pattern limits.

## Reference(s):

- [Validation Rules Reference](references/validation_rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python code examples and structured validation report data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce pandas-based profiling summaries, schema validation errors, and anomaly reports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
