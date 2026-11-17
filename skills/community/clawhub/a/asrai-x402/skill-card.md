## Description:

Provides crypto market analysis, screeners, sentiment, forecasts, and trading insights through paid Asrai x402 calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abuzerasr](https://clawhub.ai/user/abuzerasr)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users use Asrai to review cryptocurrency market signals, technical analysis, sentiment, forecasts, and exchange positions before making decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exposure of wallet credentials can result in financial loss.

Mitigation: Review before installing; use only a dedicated low-balance wallet and never place its private key in URLs or shared environment files.

Risk: Exchange API credentials can expose account data or enable unauthorized activity.

Mitigation: Use read-only exchange API keys with trading and withdrawals disabled.

Risk: Running an unreviewed package with wallet or exchange secrets increases credential exposure.

Mitigation: Pin and review the asrai-mcp package version before giving it access to secrets.

## Reference(s):

- [Asrai x402 endpoint reference](artifact/references/endpoints.md)
- [Asrai agent documentation](https://asrai.me/agents)
- [Asrai MCP package](https://www.npmjs.com/package/asrai-mcp)
- [x402 protocol](https://x402.org)
- [ClawHub skill listing](https://clawhub.ai/abuzerasr/skills/asrai-x402)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown analysis with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some analysis calls debit USDC from the user's wallet.]

## Skill Version(s):

2.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
