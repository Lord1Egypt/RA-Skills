## Description: <br>
Database Skill helps agents manage metadata, analyze data, prepare governed database changes, diagnose operations issues, and run health inspections for Volcengine databases and supported external MySQL/PostgreSQL databases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Database operators, data analysts, and developers use this skill to inspect database assets, run read-only queries and BI analysis, generate reports, troubleshoot performance or availability issues, and prepare DML/DDL change tickets through governed workflows. <br>

### Deployment Geography for Use: <br>
Volcengine-supported regions listed by the skill: Shanghai, Beijing/Langfang, Guangzhou, Hong Kong, Johor, and Jakarta. <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to Volcengine or database credentials and can reach live database resources. <br>
Mitigation: Install only when the publisher is trusted, use least-privilege accounts, and avoid production credentials when possible. <br>
Risk: Database change workflows and kill-process style operations can affect live systems if reviewed poorly. <br>
Mitigation: Review DML, DDL, and process-termination actions before execution and keep change operations within the documented approval or ticket flow. <br>
Risk: Query results, reports, and intermediate analysis data may persist locally after sensitive work. <br>
Mitigation: Clean generated /tmp files, DuckDB artifacts, workspace reports, screenshots, and .env artifacts after sensitive tasks. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/volcengine-skills/database-skill) <br>
- [Metadata Query API Reference](references/api/metadata-query.md) <br>
- [Operations API Reference](references/api/ops.md) <br>
- [Analysis Workflow](references/analysis/index.md) <br>
- [Development Change Workflow](references/develop/index.md) <br>
- [Operations Diagnosis Router](references/ops/index.md) <br>
- [Health Inspection Workflow](references/ops/health-inspection.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses, SQL/code snippets, shell commands, JSON-like API results, HTML reports, and PNG screenshots.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local query result artifacts, DuckDB files, workspace reports, screenshots, and configuration updates when the workflow requires them.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
