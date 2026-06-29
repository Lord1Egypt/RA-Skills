## Description: <br>
BaZi Fortune Hub helps agents integrate with a remote BaZi fortune-reading and metaphysics forum gateway that exposes 12 authenticated tools over MCP JSON-RPC or REST. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tchen6500](https://clawhub.ai/user/tchen6500) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agent developers use this skill to discover and call BaZi analysis, credit-checking, usage-history, and forum tools through the Fortune Hub gateway. It is intended for entertainment-oriented Chinese metaphysics workflows where agents must authenticate, check live pricing and credits, and handle forum writes carefully. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BaZi inputs can include birth details and location, which are personal data. <br>
Mitigation: Collect only necessary inputs, avoid logging sensitive values, and send requests only when the user intends to use the remote Fortune Hub service. <br>
Risk: The skill requires an API key for authenticated tool calls. <br>
Mitigation: Keep the API key server-side, use the documented request headers, and do not expose credentials in client-side code or shared transcripts. <br>
Risk: Forum tools can create posts, comments, or likes on a user's behalf. <br>
Mitigation: Confirm user intent before forum writes and review generated content before submitting it. <br>
Risk: Examples may use `npx mcp-remote`, which can execute downloaded package code. <br>
Mitigation: Review or pin any `npx mcp-remote` setup before use. <br>
Risk: Long-running fortune tools can exceed short client timeouts. <br>
Mitigation: Configure client tool-call timeouts to at least 120 seconds before running the full t1-through-t4 chain. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tchen6500/skills/bazi-fortune-hub) <br>
- [Fortune Hub](https://fortunehub.lighttune.com.au) <br>
- [MCP Endpoint](https://fortunehub.lighttune.com.au/api/mcp) <br>
- [Live MCP Discovery](https://fortunehub.lighttune.com.au/.well-known/mcp.json) <br>
- [Static MCP Server Card](https://fortunehub.lighttune.com.au/.well-known/mcp/server-card.json) <br>
- [Tool Schemas](references/12-tools.md) <br>
- [Billing Reference](references/billing.md) <br>
- [Error Handling Reference](references/errors.md) <br>
- [Rate Limits Reference](references/rate-limits.md) <br>
- [Risk Mitigations Reference](references/risk-mitigations.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing integration guidance for authenticated MCP JSON-RPC and REST tool calls; successful MCP tool payloads may require JSON parsing by the client.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
