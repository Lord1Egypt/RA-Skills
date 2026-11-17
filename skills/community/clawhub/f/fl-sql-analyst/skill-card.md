## Description:

SQL Data Analyst translates plain-English data questions into SQL for SQLite, PostgreSQL, MySQL, and CSV-backed local analysis, then returns formatted results with explanations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philipstark](https://clawhub.ai/user/philipstark)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, product managers, founders, and analysts use this skill to explore databases or CSVs in plain English, review generated SQL, and receive concise results and insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run read queries against databases or imported CSVs chosen by the user, which may expose sensitive data or produce misleading results if the SQL is incorrect.

Mitigation: Review generated SQL before use on sensitive systems, keep write operations behind explicit confirmation, and disable or avoid auto-execute when manual approval is required.

Risk: Imported data, schema caches, saved queries, exports, and query logs may be stored locally and can contain confidential information.

Mitigation: Periodically clear local schema caches, imported tables, saved queries, exports, and query logs when they may contain confidential information.

Risk: Database access depends on the credentials and connection scope provided by the user.

Mitigation: Use least-privilege database accounts and environment variables for passwords, and avoid plaintext credentials in configuration files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/philipstark/skills/fl-sql-analyst)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with SQL code blocks, formatted result tables, summaries, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce generated SQL, query explanations, analysis summaries, saved-query guidance, CSV import or export guidance, and local database configuration notes.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
