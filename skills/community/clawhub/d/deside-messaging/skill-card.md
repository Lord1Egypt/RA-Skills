## Description: <br>
Use Deside MCP for wallet-to-wallet Solana DMs, public identity lookup, and agent directory search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[desideapp](https://clawhub.ai/user/desideapp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to access Deside's MCP server for wallet-to-wallet Solana direct messages, conversation history, public wallet identity lookup, and visible agent directory search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-authenticated messaging access can expose direct-message history or let an agent send messages from the authenticated wallet. <br>
Mitigation: Install only if the user trusts Deside's MCP service, grant the narrowest OAuth scope needed, and require explicit confirmation before sending a DM or marking messages as read. <br>
Risk: Realtime DM notifications depend on the MCP session remaining open and should not be treated as guaranteed delivery in every runtime situation. <br>
Mitigation: Use list_conversations and read_dms as fallback or resync paths when realtime notifications are unavailable or interrupted. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/desideapp/deside-messaging) <br>
- [Deside MCP endpoint](https://mcp.deside.io/mcp) <br>
- [Deside OAuth authorization metadata](https://mcp.deside.io/.well-known/oauth-authorization-server) <br>
- [Deside MCP protected resource metadata](https://mcp.deside.io/.well-known/oauth-protected-resource/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires access to the Deside MCP endpoint and OAuth flow; outbound DM text is limited to 3000 characters.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
