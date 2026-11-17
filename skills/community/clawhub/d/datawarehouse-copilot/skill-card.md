## Description:

A SpecKit SDD-based data warehouse development skill that turns natural-language requirements into clarified specifications, technical plans, and implementation-ready DDL, ETL, and scheduling artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[honghaolee](https://clawhub.ai/user/honghaolee)

### License/Terms of Use:

MIT-0

## Use Case:

Data warehouse developers and business analysts use this skill to clarify warehouse requirements, collect metadata, and produce spec.md and plan.md documents. Developer users can continue through the workflow to generate task.md with traceable DDL, ETL SQL, Azkaban scheduling configuration, and data quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Metadata collection can overreach into broad database, API, web, or HDFS metadata.

Mitigation: Require explicit table allowlists or explicit user approval before whole-database or recursive metadata collection.

Risk: JDBC, OpenAPI, web, and HDFS metadata collection may involve sensitive credentials.

Mitigation: Use HTTPS, read-only scoped credentials, protected secret mechanisms, and avoid pasting live cookies or passwords into generated files or chat.

Risk: Generated DDL, ETL SQL, and scheduling configuration may affect production data if accepted without review.

Mitigation: Preserve the workflow confirmation gates, review generated artifacts, and run development-mode tests before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/honghaolee/skills/datawarehouse-copilot)
- [Publisher profile](https://clawhub.ai/user/honghaolee)
- [Workflow stages](resources/workflow-stages.md)
- [Spec template](resources/spec-template.md)
- [Plan template](resources/plan-template.md)
- [Task template](resources/task-template.md)
- [Metadata collection configuration](resources/conventions/metadata-config.md)
- [Project conventions](resources/conventions/project-conventions.md)
- [Platform conventions](resources/conventions/platform-conventions.md)
- [EasyData platform product page](https://sf.163.com/product/bp)
- [EasyData platform documentation](https://study.sf.163.com/documents/read/service_support/dsc-p-00)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documents with SQL, Java properties, YAML, and checklist sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce separate task files when task count exceeds 10.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
