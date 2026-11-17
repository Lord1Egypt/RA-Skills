## Description:

World-class data engineering skill for building scalable data pipelines, ETL/ELT systems, real-time streaming, and data infrastructure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to design, generate, validate, and optimize batch and streaming data pipelines across tools such as Airflow, Spark, dbt, Kafka, Flink, Kinesis, BigQuery, and Snowflake.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated files may overwrite paths outside the intended output folder.

Mitigation: Run generation commands only on trusted configuration files, use a disposable output directory, and inspect generated paths before executing or committing results.

Risk: Generated Docker Compose configurations may be unsafe on shared, cloud, or public-facing hosts.

Mitigation: Before starting any generated stack, bind exposed ports to localhost, add authentication, replace default credentials, and pin container image versions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wu-uk/skills/flink-query-senior-data-engineer)
- [How to Use](HOW_TO_USE.md)
- [Frameworks Reference](references/frameworks.md)
- [Templates Reference](references/templates.md)
- [Tools Reference](references/tools.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands plus generated code, JSON, YAML, properties, HTML, or text reports depending on the selected tool.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some bundled scripts can write generated files or reports to caller-supplied output paths.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports v2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
