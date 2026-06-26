## Description: <br>
Connect an agent, app, or integration to AgentPMT with an AgentPMT account Bearer Token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect MCP-compatible clients, local MCP routers, backend services, or direct REST callers to AgentPMT with an Agent Group Bearer Token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer tokens can access the Agent Group's configured tools and workflows. <br>
Mitigation: Create a least-privilege Agent Group, add only required tools and credentials, and protect the Bearer Token like a password. <br>
Risk: A copied or exposed Bearer Token may allow unauthorized AgentPMT calls. <br>
Mitigation: Do not commit tokens to source control or include them in screenshots, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [AgentPMT MCP Connection Documentation](https://www.agentpmt.com/docs/mcp-reference/connection) <br>
- [AgentPMT Programmatic Access API Documentation](https://www.agentpmt.com/docs/api-reference/programmatic-access?format=agent-md) <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with JSON, bash, HTTP, and text code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes MCP server configuration, local router commands, JSON-RPC examples, REST request examples, and troubleshooting checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
