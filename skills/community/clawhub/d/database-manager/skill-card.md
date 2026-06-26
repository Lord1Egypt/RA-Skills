## Description: <br>
Plan, operate, and recover relational databases with schema governance, safe migrations, backup drills, and incident response playbooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, database operators, and on-call engineers use this skill to plan database changes, review query and migration risk, maintain backup readiness, and respond to data integrity or availability incidents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database write, migration, DROP, TRUNCATE, bulk UPDATE, or broad DELETE operations can affect production data integrity or availability. <br>
Mitigation: Confirm production targets, backups, row counts, rollback plans, and approvals before execution; use read-only validation and explicit user confirmation for destructive operations. <br>
Risk: Local database operating notes may expose sensitive operational context if they include credentials or connection details. <br>
Mitigation: Keep ~/database-manager/ private and do not store passwords, tokens, connection strings, or private keys in the skill memory files. <br>
Risk: Backup status alone may create false confidence during recovery events. <br>
Mitigation: Run restore drills, validate recovered row counts, record measured recovery time, and keep an audit trail for recovery evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/database-manager) <br>
- [Skill homepage](https://clawic.com/skills/database-manager) <br>
- [Setup guide](setup.md) <br>
- [Query operations and change windows](query-operations.md) <br>
- [Migration and release control](migration-and-release.md) <br>
- [Backup and recovery](backup-and-recovery.md) <br>
- [Incident playbook](incident-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with checklists, templates, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local operational notes under ~/database-manager/ when the user approves.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
