## Description: <br>
Natural language to SQL. Ask questions about your data in plain English, get queries, results, and explanations. Supports SQLite, PostgreSQL, and MySQL. Import CSVs for instant ad-hoc analysis. Save frequently used queries as shortcuts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PhilipStark](https://clawhub.ai/user/PhilipStark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, product managers, analysts, and founders use this skill to ask plain-English questions about SQLite, PostgreSQL, MySQL, or CSV data and receive SQL queries, formatted results, and explanations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect schemas and run analysis queries against connected databases. <br>
Mitigation: Use read-only or least-privilege database accounts and connect only databases the user is comfortable letting an agent query. <br>
Risk: Generated SQL may be incorrect or may affect data if write operations are allowed. <br>
Mitigation: Review generated SQL before execution, require explicit confirmation for writes, and avoid production admin credentials. <br>
Risk: Local imports, exports, saved queries, schema caches, and query logs may contain sensitive business data. <br>
Mitigation: Periodically clean local analysis artifacts and handle exports according to the data owner's retention and privacy requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/PhilipStark/fl-sql-analyst) <br>
- [Publisher Profile](https://clawhub.ai/user/PhilipStark) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with SQL code blocks, formatted tables, summaries, configuration guidance, and optional CSV or local data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local schema caches, query logs, saved-query configuration, SQLite imports, and exported query-result files when the host agent permits file access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
