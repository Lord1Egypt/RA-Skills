## Description:

0xArchive helps agents query historical and real-time crypto market data from 0xArchive for Hyperliquid, Hyperliquid HIP-3, Hyperliquid HIP-4, Hyperliquid Spot, and Lighter.xyz using API-key-authenticated curl commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xfantommenace](https://clawhub.ai/user/0xfantommenace)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, traders, and analysts use this skill in SKILL.md-compatible agents to retrieve 0xArchive market data, orderbooks, trades, candles, funding rates, open interest, liquidations, outcome-market data, spot pairs, WebSocket stream guidance, and data-quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an 0xArchive API key, and command or WebSocket usage can expose long-lived credentials through logs, shell history, or process listings.

Mitigation: Use scoped and rotatable API keys, keep keys in approved secret storage or environment variables, avoid embedding keys in WebSocket URLs, and revoke exposed keys promptly.

Risk: The skill documents wallet-message signing, API key revocation, and paid subscription flows that can affect wallet access, service access, or funds.

Mitigation: Require explicit human approval before signing wallet messages, revoking keys, or starting paid subscriptions, and verify transaction details in the wallet before approval.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/0xfantommenace/skills/0xarchive)
- [0xArchive API base](https://api.0xarchive.io/v1/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, API paths, tables, and JSON response examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OXARCHIVE_API_KEY for authenticated 0xArchive API calls.]

## Skill Version(s):

1.10.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
