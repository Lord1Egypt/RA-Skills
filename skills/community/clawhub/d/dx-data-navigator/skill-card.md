## Description:

Query Developer Experience (DX) data via the DX Data MCP server PostgreSQL database for productivity metrics, team performance, pull request and code review metrics, deployment frequency, incident data, AI tool adoption, survey responses, DORA metrics, and other engineering analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiao1804](https://clawhub.ai/user/xiao1804)

### License/Terms of Use:


## Use Case:

Developers, engineering managers, and DX analysts use this skill to ask an agent for focused SQL guidance and analysis patterns over DX Data Cloud tables. It supports team-level productivity, survey, pull request, deployment, incident, AI adoption, issue, catalog, pipeline, and code quality analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can steer agents into broad queries over sensitive employee emails, identity mappings, AI adoption data, productivity metrics, and survey responses.

Mitigation: Use least-privilege read-only database credentials, prefer aggregate team-level queries, and require a clear business reason before querying individual-level data.

Risk: The security verdict is suspicious because privacy and scope guardrails are limited for sensitive DX analytics.

Mitigation: Install only from a trusted, pinned, internally reviewed source and review the skill before deployment.

## Reference(s):

- [Dx Data Navigator on ClawHub](https://clawhub.ai/xiao1804/skills/dx-data-navigator)
- [Developer Experience Core Tables](references/developer-experience.md)
- [Teams and Users](references/teams-users.md)
- [Pull Requests and Code Review](references/pull-requests.md)
- [Deployments and Incidents](references/deployments-incidents.md)
- [AI Tools and Adoption](references/ai-tools.md)
- [Issue Tracking](references/jira.md)
- [Service Catalog](references/catalog.md)
- [Pipelines and Code Quality](references/pipelines-quality.md)
- [Issues](references/issues-github.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with SQL and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce SQL query examples for the DX Data MCP server; query results can include sensitive employee, identity, survey, and productivity data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
