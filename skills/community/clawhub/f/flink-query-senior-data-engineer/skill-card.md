## Description: <br>
World-class data engineering skill for building scalable data pipelines, ETL/ELT systems, real-time streaming, and data infrastructure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to design, generate, validate, and optimize batch and streaming data pipelines across tools such as Airflow, Spark, Kafka, Flink, dbt, Kinesis, Snowflake, S3, Docker, and related data quality workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated pipeline, Kafka, Snowflake, S3, Docker, and Terraform-style artifacts may be incomplete or inappropriate for a specific production environment. <br>
Mitigation: Review generated artifacts, run them in a least-privilege test environment, and adapt them to local platform, security, and reliability requirements before production use. <br>
Risk: Prompts, examples, or templates may expose sensitive datasets, passwords, tokens, or full production connection strings. <br>
Mitigation: Use redacted examples, environment variables, and secret managers; do not paste real credentials or sensitive production data into skill prompts or templates. <br>
Risk: Streaming quality validation behavior may rely on simulator or reference logic rather than verified live integrations. <br>
Mitigation: Treat streaming quality validator outputs as reference results until Kafka, Schema Registry, Kinesis, and monitoring integrations are tested against real systems. <br>
Risk: Production-style monitoring and security templates may be under-scoped or misleading. <br>
Mitigation: Have platform and security reviewers validate monitoring coverage, alert thresholds, access controls, and deployment settings before operational adoption. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/flink-query-senior-data-engineer) <br>
- [Publisher profile](https://clawhub.ai/user/wu-uk) <br>
- [Frameworks reference](references/frameworks.md) <br>
- [Templates reference](references/templates.md) <br>
- [Tools reference](references/tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated JSON, YAML, properties, Python, Java, Docker Compose, and Terraform-style artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated artifacts should be reviewed before use in production data systems.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
