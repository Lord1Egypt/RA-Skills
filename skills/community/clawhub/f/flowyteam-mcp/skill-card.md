## Description: <br>
Manage FlowyTeam projects, tasks, OKRs, KPIs, HR, CRM, finance, support tickets, attendance, and more via MCP - 34 tools for complete workspace management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flowy-team](https://clawhub.ai/user/flowy-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, managers, and workspace administrators use this skill through an MCP-compatible agent to read and manage FlowyTeam projects, tasks, OKRs, KPIs, HR, CRM, finance, support tickets, attendance, and related records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and modify FlowyTeam workspace records, including HR, CRM, finance, support, attendance, and project data. <br>
Mitigation: Install only when agent access to the workspace is intended, use an Employee or otherwise limited-permission token, and request an Admin token only for explicitly admin-scoped tasks. <br>
Risk: Create, update, delete, account setup, or credential-retrieval actions could change business records or expose sensitive credentials if invoked without deliberate user intent. <br>
Mitigation: Require explicit confirmation in the current conversation before every create, update, or delete request, avoid password login in shared chats or CI, and revoke the token when the integration is no longer needed. <br>


## Reference(s): <br>
- [FlowyTeam Website](https://flowyteam.com) <br>
- [FlowyTeam MCP Docs](https://flowyteam.com/get/mcp-server) <br>
- [FlowyTeam MCP API Reference](https://flowyteam.com/get/mcp-docs) <br>
- [ClawHub Skill Page](https://clawhub.ai/flowy-team/flowyteam-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration, and MCP tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a FlowyTeam API token for authenticated workspace tools.] <br>

## Skill Version(s): <br>
1.1.8 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
