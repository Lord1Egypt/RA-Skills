## Description: <br>
Guides agents and users through designing and implementing a flexible SQLite soft-schema database for semi-structured, multi-source knowledge-base data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mars2003](https://clawhub.ai/user/mars2003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent users use this skill to design SQLite-backed archives and knowledge bases for personal notes, reports, policies, forms, event logs, and multi-source records. It provides discovery prompts, schema templates, workflow guidance, and Python command-line scripts for archiving, querying, importing, exporting, and managing records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local SQLite databases, copied reports, backups, and exported JSON or CSV files may contain sensitive user data. <br>
Mitigation: Confirm the database path and export destination before execution, and keep generated databases, copied reports, backups, and exports out of version control when they contain sensitive information. <br>
Risk: Custom extractor code configured with FLEXIBLE_EXTRACTOR or --extractor runs as trusted local Python code. <br>
Mitigation: Use only extractor modules from trusted sources and review their behavior before allowing an agent to execute them. <br>
Risk: SQLite full-text search and LIKE fallback may be incomplete or slow for Chinese text or larger datasets. <br>
Mitigation: Test recall with representative short phrases, assess LIKE performance at the expected data volume, and use a dedicated search engine or Chinese tokenizer when SQLite FTS is insufficient. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mars2003/flexible-database-design) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>
- [FlexibleDatabase API](docs/API.md) <br>
- [SQLite Schema Template](references/schema_template.sql) <br>
- [Business View Examples](references/view_examples.sql) <br>
- [Chinese Full-Text Search Notes](references/fulltext_chinese.md) <br>
- [Schema Migration Examples](references/migrations/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with SQL, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local SQLite schema guidance and command-line workflow instructions; Python scripts may create, query, export, and update local database files when executed by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
