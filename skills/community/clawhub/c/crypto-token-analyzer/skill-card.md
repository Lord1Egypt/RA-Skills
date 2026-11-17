## Description:

Analyze a cryptocurrency token by contract address and chain, fetching market, liquidity, security, and trend signals from DexScreener, GoPlus, and block explorers to provide a bullish, bearish, or uncertain view with position strategy guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sqxy090123](https://clawhub.ai/user/sqxy090123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and crypto market researchers use this skill to analyze a token from its contract address and chain using live market data, public security checks, and explorer context. The skill returns concise risk notes, trend interpretation, and holder or watcher strategy guidance in the conversation language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask the agent to call third-party crypto data APIs using user-supplied token addresses.

Mitigation: Install only when third-party API contact for queried token addresses is acceptable, and validate chain IDs and token address formats before running API calls.

Risk: Shell curl commands built from malformed or untrusted address strings can increase execution and data-quality risk.

Mitigation: Use strict address validation and a structured HTTP client where possible instead of directly interpolating untrusted values into shell commands.

## Reference(s):

- [Data Sources & Endpoints](references/data-sources.md)
- [Security Checklist](references/security-checklist.md)
- [DexScreener API](https://api.dexscreener.com)
- [GoPlus Token Security API](https://api.gopluslabs.io/api/v1/token_security/{chain_id}?contract_addresses={address})
- [ClawHub Skill Page](https://clawhub.ai/sqxy090123/skills/crypto-token-analyzer)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, guidance]

**Output Format:** [Markdown or natural-language response with optional inline shell commands and structured token analysis sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should match the conversation language and include a risk note that crypto analysis is not investment advice.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
