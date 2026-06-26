## Description: <br>
Universal AI resource registry — search and invoke agents, MCP servers, and APIs through a single MCP endpoint. Includes Telegram content search, Google search, X/Twitter search, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agent3-666](https://clawhub.ai/user/agent3-666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use Agent3 Hub to connect an MCP client to a remote registry, search for agents and resources, and invoke registered agents, MCP servers, and APIs from a single endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad remote gateway access can invoke third-party agents, APIs, and search services with downstream trust and privacy risk. <br>
Mitigation: Verify each resource before invoking it, avoid sending secrets or regulated data through the hub, and require explicit approval for generic invoke or register actions. <br>
Risk: The Agent3 API key is an account credential. <br>
Mitigation: Store AGENT3_API_KEY securely and avoid exposing it in shared configs, logs, or prompts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agent3-666/agent3-hub) <br>
- [Agent3 Registry](https://hub.agent3.me) <br>
- [Agent3 Docs](https://hub.agent3.me/docs) <br>
- [Agent3 MCP Endpoint](https://hub.agent3.me/api/mcp) <br>
- [Agent3 API Key Signup](https://hub.agent3.me/auth/signup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Configuration, Shell commands, Code] <br>
**Output Format:** [MCP tool responses with JSON configuration examples, bash curl commands, and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENT3_API_KEY for authenticated tools; public list and initialize tools are available without authentication.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
