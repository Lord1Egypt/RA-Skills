## Description:

Automate Bitbucket repositories, pull requests, branches, issues, and workspace management via Rube MCP (Composio). Always search tools first for current schemas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sohamganatra](https://clawhub.ai/user/sohamganatra)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to operate Bitbucket workspaces and repositories through Rube MCP, including pull request workflows, branch creation, issue management, repository administration, and reviewer lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rube MCP access can operate on connected Bitbucket accounts or workspaces.

Mitigation: Review OAuth scopes during connection and use the least-privileged Bitbucket account practical.

Risk: Repository and issue deletion operations are permanent.

Mitigation: Require explicit user confirmation before calling Bitbucket delete tools.

Risk: Stale tool parameters can cause incorrect Bitbucket operations.

Mitigation: Search Rube MCP tools first and use the current returned schemas before running workflows.

## Reference(s):

- [Rube MCP endpoint](https://rube.app/mcp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with MCP tool names, parameter notes, and workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based on current Rube MCP tool schemas and may include Bitbucket operation plans or MCP tool calls.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
