## Description:

Binance Spot request using the Binance API. Authentication requires API key and secret key. Supports testnet and mainnet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viktor-huang](https://clawhub.ai/user/viktor-huang)

### License/Terms of Use:

MIT

## Use Case:

Developers and trading automation users use this skill to query Binance Spot market data, inspect account and order state, and prepare authenticated Spot API requests for testnet or mainnet workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Binance API keys or secrets could be exposed if stored in plaintext workspace files.

Mitigation: Use a dedicated secret manager or local environment variables, avoid synced or repository files, and rotate any key that was used during testing.

Risk: Authenticated mainnet endpoints can place or cancel real Spot orders.

Mitigation: Prefer testnet first, require explicit user confirmation for mainnet transactions, disable withdrawals, use tightly scoped API permissions, and enable IP allowlisting.

## Reference(s):

- [Binance Spot Skill on ClawHub](https://clawhub.ai/viktor-huang/skills/binance-official-spot)
- [Binance Authentication](references/authentication.md)
- [Binance Spot API](https://api.binance.com)
- [Binance Spot Testnet](https://testnet.binance.vision)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated endpoints require Binance API credentials and signed request parameters.]

## Skill Version(s):

1.0.1 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
