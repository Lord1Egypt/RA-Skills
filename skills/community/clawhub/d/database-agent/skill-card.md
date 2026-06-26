## Description: <br>
Database Agent helps Java backend developers analyze slow SQL, check schema standards, validate data corrections, and generate compliant test data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ningwang770](https://clawhub.ai/user/ningwang770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database engineers use this skill to investigate database performance issues, review schema quality, prepare safer data correction workflows, and generate realistic test data for Java backend projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad database access with weak built-in limits. <br>
Mitigation: Use least-privilege database accounts, prefer read-only credentials for analysis, and avoid production credentials unless each SQL action is manually reviewed. <br>
Risk: Raw queries or result output may expose sensitive database contents in the agent session or logs. <br>
Mitigation: Do not use raw query paths on sensitive data unless that exposure is acceptable; redact or limit query results before sharing them with the agent. <br>
Risk: Generated data correction or optimization SQL can modify large amounts of data or affect production performance. <br>
Mitigation: Test scripts in non-production first, require explicit review for UPDATE or DELETE statements, and generate backup or rollback SQL before execution. <br>


## Reference(s): <br>
- [SQL Optimization Rules](references/sql_optimization_rules.md) <br>
- [Database Design Standards and Naming Conventions](references/database_standards.md) <br>
- [Safe Database Operation Guidelines](references/safe_operation_guidelines.md) <br>
- [Test Data Generation Patterns](references/test_data_patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON reports, SQL scripts, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include database analysis findings, generated rollback or backup SQL, schema compliance reports, and test data configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
