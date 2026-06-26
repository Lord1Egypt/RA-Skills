## Description: <br>
Kole By SyneHQ helps agents query connected databases with SQL, PostgreSQL commands, natural language, and schema-discovery workflows through SyneHQ's Kole MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theboringhumane](https://clawhub.ai/user/theboringhumane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to configure SyneHQ Kole access, inspect database connections and schemas, and run SQL or natural-language data analysis against connected databases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad access to real databases, including write or administrator SQL paths. <br>
Mitigation: Use read-only, least-privilege database credentials by default and require explicit approval for INSERT, UPDATE, DELETE, DROP, migrations, exports, maintenance commands, or production access. <br>
Risk: Broad activation guidance may cause the skill to be used for database work before the target connection or environment is confirmed. <br>
Mitigation: Verify the intended connection, database, and environment before executing queries, and test connections before running analysis or changes. <br>
Risk: The SyneHQ API key grants access to connected databases through the configured account. <br>
Mitigation: Store the API key only in environment variables or an approved secret manager, avoid committing it to version control, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [Query Patterns Reference](references/query-patterns.md) <br>
- [SyneHQ Documentation](https://docs.synehq.com) <br>
- [SyneHQ Kole MCP Source](https://github.com/synehq/kole-mcp) <br>
- [SyneHQ Kole MCP npm Package](https://www.npmjs.com/package/@synehq/kole-mcp) <br>
- [ClawHub Skill Listing](https://clawhub.ai/theboringhumane/data-analysis-synehq) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with SQL, JavaScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured SyneHQ Kole MCP server and SYNEHQ_API_KEY before database queries can run.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata; artifact frontmatter reports 1.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
