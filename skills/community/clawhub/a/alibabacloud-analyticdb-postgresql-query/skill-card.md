## Description: <br>
Helps shell-capable agents connect to AnalyticDB PostgreSQL with psql, generate guarded read-only SQL, return query results, and export CSV files after explicit user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data analysts, business users, and developers use this skill to ask natural-language questions against an AnalyticDB PostgreSQL database through a DBA-configured semantic model. The agent can prepare scoped SQL, request approval, execute read-only psql queries, and export approved results for local analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Connection Guide](artifact/references/connection-guide.md) <br>
- [SQL Guide](artifact/references/sql-guide.md) <br>
- [Export Guide](artifact/references/export-guide.md) <br>
- [Semantic Model Guide](artifact/references/semantic-model-guide.md) <br>
- [Resource Group Guide](artifact/references/resource-group-guide.md) <br>
- [ADBPG psql Documentation](https://help.aliyun.com/zh/analyticdb/analyticdb-for-postgresql/user-guide/psql) <br>
- [PostgreSQL Windows Download](https://www.postgresql.org/download/windows/) <br>


## Skill Output: <br>
**Output Type(s):** [SQL, CSV files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline SQL, shell commands, and CSV export file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires psql and database connection configuration; query execution and CSV exports require explicit user approval and may handle sensitive local data.] <br>

## Skill Version(s): <br>
0.0.1-beta.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
