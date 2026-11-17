## Description:

Plan, operate, and recover relational databases with schema governance, safe migrations, backup drills, and incident response playbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, database operators, and incident responders use this skill to plan safe schema and data changes, verify backup and restore readiness, and coordinate database incidents with documented rollback and validation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local database operations notes may capture sensitive database context if misused.

Mitigation: Keep secrets, passwords, connection strings, and private keys out of ~/database-manager/ and store only durable operational context.

Risk: Production database changes can affect reliability, latency, or data integrity when executed without review.

Mitigation: Use preflight packets, explicit confirmation for destructive operations, documented rollback paths, and verification queries before approving changes.

## Reference(s):

- [Database Manager on ClawHub](https://clawhub.ai/ivangdavila/skills/database-manager)
- [Database Manager Homepage](https://clawic.com/skills/database-manager)
- [Setup](artifact/setup.md)
- [Inventory and Governance](artifact/inventory-and-governance.md)
- [Query Operations and Change Windows](artifact/query-operations.md)
- [Migration and Release Control](artifact/migration-and-release.md)
- [Backup and Recovery](artifact/backup-and-recovery.md)
- [Incident Playbook](artifact/incident-playbook.md)
- [Reusable Templates](artifact/templates.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with checklists, templates, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local files under ~/database-manager/ when the user approves persistent database operations notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
