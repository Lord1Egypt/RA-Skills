## Description: <br>
ChatbotX MCP Server gives AI agents access to a ChatbotX workspace through Model Context Protocol tools generated from the ChatbotX OpenAPI specification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunghajung43](https://clawhub.ai/user/sunghajung43) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators connect an AI agent to a ChatbotX workspace to inspect and manage workspace resources such as contacts, tags, conversations, broadcasts, flows, sequences, integrations, and error logs. The server is intended for authenticated ChatbotX environments where the user wants agent-driven workspace automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants an AI agent broad live access to ChatbotX workspace data and actions, including contacts, conversations, tags, deletes, messages, and flow actions. <br>
Mitigation: Enable it only for trusted agents and workspaces, review the OpenAPI operations exposed by the ChatbotX instance, and use least-privilege, revocable workspace tokens where possible. <br>
Risk: Remote SSE deployment can expose workspace access if tokens, network access, or CORS settings are handled loosely. <br>
Mitigation: Prefer local stdio mode or a tightly restricted private SSE deployment, avoid putting tokens in URLs, restrict network exposure, and set narrow CORS origins. <br>
Risk: Self-signed certificate support can disable TLS verification for self-hosted instances. <br>
Mitigation: Use trusted TLS certificates in production and enable self-signed certificate mode only for controlled local or internal environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunghajung43/chatbotx) <br>
- [Model Context Protocol](https://modelcontextprotocol.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CHATBOTX_API_KEY and CHATBOTX_API_URL; supports macOS, Linux, and Windows according to ClawHub metadata.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
