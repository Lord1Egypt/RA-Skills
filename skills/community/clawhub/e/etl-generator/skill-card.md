## Description:

Generates standardized big-data ETL SQL from source table DDL for HiveSQL, MySQL, and ODPS workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexmayanjun-collab](https://clawhub.ai/user/alexmayanjun-collab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to turn source table DDL into target table DDL, ETL processing SQL, data quality checks, and field mapping notes for warehouse pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated INSERT OVERWRITE SQL can alter or replace warehouse partitions if run without review.

Mitigation: Review generated schema lookups and validate the SQL against staging tables or limited partitions before production execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alexmayanjun-collab/skills/etl-generator)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SQL, Python, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces generated SQL that should be reviewed before execution against production data.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
