## Description: <br>
Automate Bitbucket repositories, pull requests, branches, issues, and workspace management via Rube MCP (Composio). Always search tools first for current schemas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sohamganatra](https://clawhub.ai/user/sohamganatra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to manage Bitbucket repositories, pull requests, branches, issues, and workspace administration through Rube MCP after connecting a Bitbucket workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connected Bitbucket workspaces can be changed through high-impact actions such as repository or issue deletion. <br>
Mitigation: Use least-privileged Bitbucket access, review OAuth authorization, and require explicit confirmation before deletion or public-facing comments. <br>
Risk: Tool schemas and Bitbucket parameters may change or vary by operation. <br>
Mitigation: Search current Rube tool schemas before each operation and resolve workspace, repository, branch, member, pull request, and issue identifiers before making changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sohamganatra/bitbucket-automation) <br>
- [Rube MCP endpoint](https://rube.app/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown guidance with MCP tool names, workflow steps, and parameter notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Rube MCP and an active Bitbucket connection before workflows can run.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
