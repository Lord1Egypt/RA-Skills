## Description: <br>
Db Explorer helps agents connect to PostgreSQL, MySQL, SQLite, MongoDB, and Redis databases to inspect schemas, run queries, export data, and debug database issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Db Explorer to query databases, inspect schemas and performance, export results, and troubleshoot database issues from terminal-driven workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database access can expose sensitive data or affect production systems when credentials are broad. <br>
Mitigation: Use read-only credentials where possible, apply least privilege, avoid putting real passwords in chat or shell history, and confirm the target environment before running commands. <br>
Risk: Backup, restore, export, import, migration, and write operations can disclose or alter data. <br>
Mitigation: Require explicit confirmation, show the exact command first, limit exports, and use transactions or test dumps before changes. <br>
Risk: Unbounded queries or broad key scans can be slow or disruptive on large databases. <br>
Mitigation: Apply result limits by default and prefer scoped queries or safer key-scanning patterns for large datasets. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lrg913427-dot/gavin-db-explorer) <br>
- [Publisher Profile](https://clawhub.ai/user/lrg913427-dot) <br>
- [MongoDB Shell Documentation](https://www.mongodb.com/docs/mongodb-shell/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash, SQL, and database shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include database CLI commands, query snippets, and export file paths for review before execution.] <br>

## Skill Version(s): <br>
2.3.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
