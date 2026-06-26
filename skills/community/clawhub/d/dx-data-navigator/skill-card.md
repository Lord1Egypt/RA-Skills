## Description: <br>
Query Developer Experience (DX) data via the DX Data MCP server PostgreSQL database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xiao1804](https://clawhub.ai/user/Xiao1804) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineering leaders, and DX analysts use this skill to query engineering analytics across DX surveys, teams, pull requests, deployments, incidents, AI tool adoption, issue tracking, service catalog data, pipelines, and code quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to query sensitive employee, survey, productivity, AI adoption, and identity-linkage data. <br>
Mitigation: Use a read-only, least-privileged DX MCP database account and require explicit approval before retrieving names, emails, protected-user flags, individual survey answers, AI adoption status, or cross-system identity joins. <br>
Risk: Individual-level engineering metrics can be misused or overinterpreted. <br>
Mitigation: Prefer aggregate team-level reporting and review results for privacy, authorization, and context before sharing. <br>
Risk: Known data quality issues include duplicate DX survey scores, team-name typos, mostly null DX user AI adoption fields, and missing incident-service links. <br>
Mitigation: Verify team names from the source tables, aggregate duplicate survey rows as documented, prefer Copilot usage tables for AI adoption analysis, and avoid claiming service-level incident attribution when supporting links are absent. <br>


## Reference(s): <br>
- [Developer Experience (DX) Core Tables](references/developer-experience.md) <br>
- [Teams and Users](references/teams-users.md) <br>
- [Pull Requests and Code Review](references/pull-requests.md) <br>
- [Deployments and Incidents](references/deployments-incidents.md) <br>
- [AI Tools and Adoption](references/ai-tools.md) <br>
- [Issue Tracking Integration](references/jira.md) <br>
- [Service Catalog](references/catalog.md) <br>
- [Pipelines and Code Quality](references/pipelines-quality.md) <br>
- [Issues](references/issues-github.md) <br>
- [ClawHub skill page](https://clawhub.ai/Xiao1804/dx-data-navigator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with SQL examples and concise analysis guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose database queries through the DX Data MCP server and summarize results for engineering analytics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
