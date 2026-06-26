## Description: <br>
Coinversa Pulse provides read-only, API-key-authenticated crypto market intelligence for AI agents across Hyperliquid trader analytics, live market data, builder dex markets, and HIP-4 outcome contracts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nazchedz](https://clawhub.ai/user/nazchedz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and AI agent users use this skill to query Coinversa-hosted crypto market data and wallet-level analytics for research, risk review, and market monitoring without trading or wallet control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API-key-authenticated analytics queries, including wallet addresses and market research parameters, are sent to Coinversa. <br>
Mitigation: Use the skill only when that data sharing is acceptable, use a dedicated low-privilege API key where possible, and rotate the key if it may have been exposed. <br>
Risk: The local stdio setup installs and runs an external npm package. <br>
Mitigation: Use the pinned package version shown by the skill and separately verify the package source before local installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nazchedz/coinversaa-pulse) <br>
- [Coinversa website](https://coinversa.ai) <br>
- [Coinversa API documentation](https://coinversa.ai/developers) <br>
- [npm package](https://www.npmjs.com/package/@coinversaa/mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with MCP analytics responses and setup snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Coinversa API key; requests may include wallet addresses, market symbols, HIP-4 outcome IDs, time windows, usage metadata, and analytics parameters.] <br>

## Skill Version(s): <br>
0.7.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
