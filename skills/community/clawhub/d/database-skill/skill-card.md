## Description:

Database Skill helps agents work with Volcengine and supported self-managed databases for metadata discovery, data analysis, data governance, development-change workflows, operations diagnosis, and health inspection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, database operators, and data analysts use this skill to inspect database metadata, run read-only analysis, create visual reports, assess data governance signals, diagnose operational issues, and prepare governed database change requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use cloud database credentials and powerful database operations.

Mitigation: Install only after review, use least-privilege credentials, and prefer read-only credentials for analysis.

Risk: Session termination and database changes can affect live systems.

Mitigation: Disable or tightly control update_env, execute_sql, and kill_process, and require explicit human confirmation for session termination and database changes.

Risk: Local DuckDB, temporary, or workspace outputs may contain sensitive database or file-analysis data.

Mitigation: Clean or isolate local analysis outputs after use and restrict access to generated report artifacts.

## Reference(s):

- [Database Skill release page](https://clawhub.ai/volcengine-skills/skills/database-skill)
- [Metadata query API reference](references/api/metadata-query.md)
- [Operations API reference](references/api/ops.md)
- [Data analysis workflow](references/analysis/index.md)
- [Development change workflow](references/develop/index.md)
- [Operations diagnosis SOP](references/ops/index.md)
- [Health inspection SOP](references/ops/health-inspection.md)
- [Data governance references](references/metadata/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, HTML reports, PNG screenshots]

**Output Format:** [Markdown, structured text, SQL/code snippets, JSON-like command results, HTML reports, and PNG screenshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist local analysis artifacts and report files during database or file analysis workflows.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
