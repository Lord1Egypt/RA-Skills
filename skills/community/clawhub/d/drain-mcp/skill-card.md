## Description: <br>
MCP server for the Handshake58 AI marketplace where agents discover providers, open USDC payment channels on Polygon, and call AI services with off-chain signed vouchers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kimbo128](https://clawhub.ai/user/kimbo128) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agent operators use this skill to configure an MCP server that discovers Handshake58 providers, opens funded Polygon USDC payment channels, and routes agent requests through paid provider APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The external MCP package can use a wallet private key to authorize spending from the configured Polygon wallet. <br>
Mitigation: Use a fresh low-balance wallet dedicated to this skill and never provide a main wallet or seed phrase. <br>
Risk: Unused USDC in expired payment channels is not returned automatically. <br>
Mitigation: Store channel IDs, monitor channel status, and close expired channels to recover unused funds. <br>
Risk: Agent messages are sent to third-party providers selected through the marketplace. <br>
Mitigation: Review provider documentation before use and avoid sending sensitive data unless the provider is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kimbo128/drain-mcp) <br>
- [Handshake58 website](https://handshake58.com) <br>
- [Handshake58 provider directory](https://handshake58.com/directory) <br>
- [drain-mcp npm package](https://www.npmjs.com/package/drain-mcp) <br>
- [DRAIN repository listed in skill metadata](https://github.com/kimbo128/DRAIN) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON configuration and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DRAIN_PRIVATE_KEY and network access to Handshake58 endpoints, selected providers, and Polygon RPC.] <br>

## Skill Version(s): <br>
1.8.0 (source: server release metadata; skill frontmatter lists 1.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
