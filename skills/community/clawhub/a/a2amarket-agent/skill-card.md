## Description: <br>
A2A Market helps an agent buy goods, list products for sale, declare supply capabilities, and track marketplace notifications through the A2A Market API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ggqshuai-hub](https://clawhub.ai/user/ggqshuai-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to let an assistant act as a commerce helper for procurement, product listing, supply declarations, and transaction status checks. The skill requires a user-provided A2A Market API key and asks the agent to summarize marketplace activity in natural language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent authenticated marketplace authority, including actions that can create procurement or supply activity. <br>
Mitigation: Use a low-balance or scoped API key first, and require the agent to summarize and get approval before any POST, PUT, or DELETE request. <br>
Risk: The skill requires a sensitive A2A Market API key. <br>
Mitigation: Provide the key through environment variables, rotate it if exposed, and avoid sharing it in chat or logs. <br>
Risk: Webhook configuration can change where marketplace notifications are routed. <br>
Mitigation: Configure webhooks only to endpoints the user controls and confirm the target URL before updating agent settings. <br>
Risk: The optional npx MCP server is separate executable software. <br>
Mitigation: Review the package and its behavior before running it; using this markdown skill alone does not require installing that package. <br>


## Reference(s): <br>
- [A2A Market homepage](https://a2amarket.md) <br>
- [A2A Market developer platform](https://dev.a2amarket.md) <br>
- [A2A Market API base](https://api.a2amarket.md) <br>
- [ClawHub skill page](https://clawhub.ai/ggqshuai-hub/a2amarket-agent) <br>
- [Optional A2A Market MCP server package](https://www.npmjs.com/package/@hz-abyssal-heart/a2amarket-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with REST API examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include natural-language summaries of API responses, marketplace notifications, configuration steps, and user-confirmation prompts.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
