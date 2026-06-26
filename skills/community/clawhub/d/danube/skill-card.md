## Description: <br>
Connect your AI agent to a growing marketplace of services and tools through a single API key to discover, search, and execute available tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[preston-thiele](https://clawhub.ai/user/preston-thiele) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to connect to Danube, discover available marketplace services and tools, configure the MCP connection, and execute user-scoped tool workflows through a Danube API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A single Danube API key can let an agent discover and execute broad remote tool actions, including user-scoped writes. <br>
Mitigation: Require explicit user approval before writes, messages, purchases, deletions, credentialed service actions, and batch executions. <br>
Risk: Tool inputs may be sent to Danube-mediated third-party services during execution. <br>
Mitigation: Connect only needed third-party accounts and avoid sending unnecessary sensitive data in tool parameters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/preston-thiele/danube) <br>
- [Publisher Profile](https://clawhub.ai/user/preston-thiele) <br>
- [Danube Homepage](https://danubeai.com) <br>
- [Danube Dashboard](https://danubeai.com/dashboard) <br>
- [Danube Documentation](https://docs.danubeai.com) <br>
- [Danube MCP Server](https://mcp.danubeai.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and a DANUBE_API_KEY; tool actions run through Danube-mediated remote services under the authenticated user's scope.] <br>

## Skill Version(s): <br>
8.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
