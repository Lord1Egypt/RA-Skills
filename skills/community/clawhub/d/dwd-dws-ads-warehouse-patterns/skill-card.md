## Description:

Provides SQL patterns and design guidance for DWD, DWS, and ADS layered data warehouse architecture, including multi-period rollups, dimension explosion, OLAP multi-select deduplication, and historical period freezing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fang-zeqiang](https://clawhub.ai/user/fang-zeqiang)

### License/Terms of Use:

MIT-0

## Use Case:

Data engineers and analytics developers use this skill to design layered warehouse tables, generate SQL skeletons, choose aggregation patterns, and document DWD-to-DWS-to-ADS data flow with Mermaid diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SQL templates include INSERT OVERWRITE and partition placeholders that could affect production warehouse data if applied without review.

Mitigation: Review generated SQL, partition dates, and target tables through normal data change controls before execution.

Risk: Incorrect placeholder style or period-end logic can cause T-1/T-0 misalignment or incomplete-period reporting.

Mitigation: Confirm scheduler placeholder conventions and validate period boundaries against the time dimension before release.

Risk: Column order mismatch between INSERT SELECT output and DDL can silently write values into the wrong fields.

Mitigation: Compare SELECT columns with the DDL field order during code review and test writes in a non-production environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fang-zeqiang/skills/dwd-dws-ads-warehouse-patterns)
- [Publisher homepage](https://zeqiang.fun)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with SQL and Mermaid code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reference patterns and templates; generated SQL should be reviewed before warehouse execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
