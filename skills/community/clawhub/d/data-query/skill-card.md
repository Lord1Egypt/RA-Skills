## Description:

Converts natural-language data questions into validated SQL and generates deployable ECharts HTML dashboards from mounted database knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ylyuanlu](https://clawhub.ai/user/ylyuanlu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data or reporting teams use this skill to answer natural-language business data questions, validate generated SQL, and produce embeddable HTML charts or multi-chart dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships operational-looking credentials and insecure HTTP/API defaults.

Mitigation: Replace shipped credentials, use HTTPS-only API endpoints, and verify database and API accounts before installation.

Risk: Generated HTML can contain SQL and use browser session tokens.

Mitigation: Treat generated HTML as sensitive, restrict access to produced files, and review SQL before deployment.

Risk: Database access may be broader than intended if accounts are over-scoped.

Mitigation: Use read-only, least-privilege database accounts scoped to the intended schema and tenant.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ylyuanlu/skills/data-query)
- [README](README.md)
- [SQL generation rules](knowledge/shared/sql_generation_rules.md)
- [DM SQL dialect specification](database_specs/dialect/DM.md)
- [MySQL SQL dialect specification](database_specs/dialect/MySQL.md)
- [Oracle SQL dialect specification](database_specs/dialect/Oracle.md)
- [ShardingSphere routing rules](database_specs/sharding/ROUTING_RULES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown, SQL and JavaScript code snippets, JSON query results, and generated HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local preview and deployable HTML dashboard files after SQL validation.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
