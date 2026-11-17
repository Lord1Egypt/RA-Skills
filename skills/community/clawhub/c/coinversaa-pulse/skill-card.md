## Description:

Coinversaa Pulse provides read-only, API-key-authenticated crypto market intelligence for Hyperliquid trader analytics, live market data, HIP-4 outcome contracts, builder dex markets, risk data, and wallet-level research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nazchedz](https://clawhub.ai/user/nazchedz)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to query read-only Hyperliquid market data, trader behavior, cohort analytics, HIP-4 outcome contracts, liquidation data, open interest, builder dex markets, and wallet-level trading history through MCP-compatible clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local setup runs an external npm MCP server.

Mitigation: Prefer the hosted endpoint when appropriate, or inspect the pinned npm package before local use.

Risk: The skill sends API-key-authenticated market, wallet, cohort, HIP-4, time-window, and analytics request data to Coinversa's hosted API.

Mitigation: Use a separate Coinversa API key with the minimum access needed and avoid submitting private, sensitive, or nonpublic information.

Risk: Users may confuse this read-only analytics skill with trading or wallet-control functionality.

Mitigation: Do not provide private keys, seed phrases, wallet signatures, exchange credentials, wallet approvals, or Hyperliquid agent approvals to this skill.

Risk: Syncer-backed recent-intelligence tools may lag real-time market state.

Mitigation: Treat syncer-backed analytics as research signals and cross-check venue-reported open interest with official open-interest tools where available.

## Reference(s):

- [Coinversa Website](https://coinversa.ai)
- [Coinversa API Docs](https://coinversa.ai/developers)
- [Coinversa MCP Endpoint](https://mcp.coinversa.ai/mcp)
- [@coinversaa/mcp-server npm Package](https://www.npmjs.com/package/@coinversaa/mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and text responses with optional shell commands and MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are read-only analytics responses; all tools require a Coinversa API key and may be subject to access-tier limits.]

## Skill Version(s):

0.7.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
