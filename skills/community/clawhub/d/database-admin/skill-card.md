## Description: <br>
Comprehensive database administration, schema management, data operations, and optimization for PostgreSQL-oriented workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericyang1234](https://clawhub.ai/user/ericyang1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database administrators use this skill to create and migrate PostgreSQL schemas, bulk insert data, optimize queries, handle JSONB and BIGINT fields, and manage backups or restores. It is intended for database administration assistance and should be reviewed before operating on live systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release exposes live-looking PostgreSQL credentials and connection details for a specific RoadFlow database. <br>
Mitigation: Treat the exposed password as compromised, rotate it, remove hardcoded connection details, and use environment variables or a secret manager before deployment. <br>
Risk: The skill includes scripts and guidance that can change schemas, restore data, clean up backups, benchmark queries, or perform bulk updates. <br>
Mitigation: Run with least-privilege credentials, require explicit confirmation or dry-runs for destructive operations, and review generated SQL before applying it to live databases. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ericyang1234/database-admin) <br>
- [Database Schema Guidelines](references/DB_SCHEMA.md) <br>
- [Usage Guide](references/USAGE_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with SQL, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce database schema changes, SQL statements, backup or restore commands, and operational recommendations.] <br>

## Skill Version(s): <br>
2.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
