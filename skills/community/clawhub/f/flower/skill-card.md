## Description: <br>
Manage projects and tasks with the Flower project management API via MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parker-xferops](https://clawhub.ai/user/parker-xferops) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and project teams use this skill to create, update, search, move, and delete Flower tasks, projects, columns, comments, team memberships, and notification preferences through an MCP client. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP server can create, update, move, or delete project-management records and change team membership or notification settings. <br>
Mitigation: Review destructive or permission-changing actions before execution and use a Flower API token with the minimum required permissions. <br>
Risk: The skill runs the third-party @xferops/flower-mcp package and sends requests to the configured Flower service. <br>
Mitigation: Verify that the package source and configured Flower URL are trusted, and pin a known package version when deploying in controlled environments. <br>


## Reference(s): <br>
- [Flower skill page](https://clawhub.ai/parker-xferops/flower) <br>
- [Flower API service](https://flower.xferops.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Flower API token and the @xferops/flower-mcp MCP server.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
