## Description: <br>
Database Engineering Mastery provides database design, optimization, migration, monitoring, backup, recovery, and operational guidance for PostgreSQL, MySQL, SQLite, and general SQL patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, database engineers, and agents use this skill to design schemas, tune queries, plan migrations, set up monitoring, create backup strategies, and follow database operations runbooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Operational database commands may have high impact on live systems, including query termination, replication-slot changes, VACUUM FULL, restore, delete, or migration steps. <br>
Mitigation: Require explicit human approval, verify the target environment, prefer read-only diagnostics first, and avoid high-impact commands on production without a maintenance or incident plan. <br>
Risk: Schema migrations and recovery actions can cause data loss, downtime, or application incompatibility if applied without preparation. <br>
Mitigation: Test against a copy of production data, confirm backups and rollback steps, and review generated SQL before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1kalin/afrexai-database-engineer) <br>
- [Publisher Profile](https://clawhub.ai/user/1kalin) <br>
- [AfrexAI Context Packs](https://afrexai-cto.github.io/context-packs/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with SQL, YAML, INI, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational checklists, scoring rubrics, SQL templates, and database administration runbooks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
