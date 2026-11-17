## Description: <br>
Db Connector Free provides database connection and basic operations guidance for developers, covering connection pools, transactions, schema changes, query patterns, data integrity, and backup practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and small teams use this skill to get practical database connection, SQL review, transaction, schema change, and backup guidance during application development and initial incident triage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests command execution and file write authority for database diagnostics without clear scoping or user controls. <br>
Mitigation: Review proposed commands and file changes before execution, run in a constrained agent session, and grant only the tools needed for the specific diagnostic task. <br>
Risk: Live database or network diagnostics may expose production credentials or affect sensitive systems. <br>
Mitigation: Use non-production credentials where possible, keep credentials out of skill files and prompts, and require explicit user approval before connecting to production databases. <br>
Risk: Database operational guidance can be incomplete or unsuitable for a specific engine, version, workload, or recovery objective. <br>
Mitigation: Validate recommendations against the target database documentation, test schema and backup changes in staging, and have a qualified operator review production changes. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/db-connector-free) <br>
- [Publisher homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with optional JSON response examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose database diagnostics; users should review commands and avoid exposing production credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
