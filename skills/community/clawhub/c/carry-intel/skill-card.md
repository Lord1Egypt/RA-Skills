## Description:

Read-only Hyperliquid funding data via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thearkoftech](https://clawhub.ai/user/thearkoftech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-data users can screen Hyperliquid funding opportunities and read dated funding digests through a remote API or MCP server. Paid requests require explicit user authorization; the skill does not place trades or manage funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid remote data requests can spend USDC or expose wallet credentials if payment challenges are trusted without validation.

Mitigation: Require explicit approval or a capped budget, verify the exact payment route and challenge before signing, use a dedicated low-balance wallet, and never provide wallet secrets to the service.

Risk: Funding screens may be mistaken for guaranteed returns or executable trading advice.

Mitigation: Treat results as market data only; independently assess fees, slippage, liquidation, venue risk, and current account status before financial decisions.

## Reference(s):

- [Carry Intel ClawHub listing](https://clawhub.ai/thearkoftech/skills/carry-intel)
- [Carry Intel MCP service](https://devbox.tail873466.ts.net:10000/mcp)
- [Historical funding-rate reports (referenced by the skill; not verified release provenance)](https://github.com/TheArkofTech/hl-carry-public)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration guidance]

**Output Format:** [JSON market-data responses, Markdown digests, and MCP configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only funding observations and screened candidates; paid requests use user-authorized USDC micropayments.]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
