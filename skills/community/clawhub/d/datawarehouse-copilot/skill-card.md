## Description: <br>
DW-Copilot guides data warehouse teams through a SpecKit SDD workflow that turns natural-language requirements into spec.md, plan.md, and deployable DDL, ETL, and scheduler outputs using project conventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[honghaolee](https://clawhub.ai/user/honghaolee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data warehouse developers and business or product stakeholders use this skill to clarify requirements, collect metadata, and produce traceable spec.md and plan.md documents. Data warehouse developers can continue to generate executable task.md content with DDL, ETL SQL, scheduler configuration, and data quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated DDL, INSERT OVERWRITE SQL, or scheduler configuration could affect production warehouse data if used without review. <br>
Mitigation: Review generated code and configuration in a development environment before production use. <br>
Risk: Metadata collection may require database, API, web, or HDFS credentials. <br>
Mitigation: Use read-only or least-privileged credentials, prefer environment variables for secrets, avoid saving cookies or keytabs in project files, and limit collection scope. <br>
Risk: Ambiguous requirements or missing metadata can lead to incorrect warehouse specifications or transformations. <br>
Mitigation: Follow the skill's required clarification and approval checkpoints before generating plan.md or task.md. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/honghaolee/datawarehouse-copilot) <br>
- [Workflow stages](resources/workflow-stages.md) <br>
- [Spec template](resources/spec-template.md) <br>
- [Plan template](resources/plan-template.md) <br>
- [Task template](resources/task-template.md) <br>
- [Metadata collection configuration](resources/conventions/metadata-config.md) <br>
- [Project conventions](resources/conventions/project-conventions.md) <br>
- [Platform conventions](resources/conventions/platform-conventions.md) <br>
- [EasyData platform](https://sf.163.com/product/bp) <br>
- [EasyData platform documentation](https://study.sf.163.com/documents/read/service_support/dsc-p-00) <br>
- [Azkaban variable reference](https://study.sf.163.com/documents/read/service_support/dsc-p-a-0176) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown documents with SQL and scheduler configuration code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce spec.md and plan.md for all users; may produce task.md with DDL, ETL SQL, Azkaban configuration, and data quality checks for data warehouse developers.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
