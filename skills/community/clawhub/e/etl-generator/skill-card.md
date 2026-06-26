## Description: <br>
Generates standardized ETL SQL from source table DDL for HiveSQL, MySQL, and ODPS workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexmayanjun-collab](https://clawhub.ai/user/alexmayanjun-collab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to turn source table DDL into target table DDL, ETL processing SQL, data quality checks, and field mapping documentation for big data pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated INSERT OVERWRITE statements can affect target tables or partitions if used without review. <br>
Mitigation: Review target table names, partitions, date filters, and database/table values before execution, and use staging or a dry run before production. <br>
Risk: Table-name workflows may inspect schemas beyond the intended ETL task. <br>
Mitigation: Allow schema lookup only for tables the user intends the agent to inspect. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexmayanjun-collab/etl-generator) <br>
- [Skill README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces generated SQL and documentation for review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
