## Description:

Trade and monitor ApeX perpetual futures, including portfolio status, market analysis, order execution, cancellations, and trade reward enrollments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joshlin111](https://clawhub.ai/user/joshlin111)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to monitor ApeX perpetual futures portfolios, analyze crypto market conditions, and prepare or execute ApeX trading commands through an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place or cancel live ApeX perpetual futures orders using high-impact credentials.

Mitigation: Use testnet first and require explicit manual confirmation of symbol, side, size, price, and account context before any order or cancel-all command runs.

Risk: ApeX API credentials and the Omni seed grant sensitive trading access.

Mitigation: Keep credentials local, out of shared or synced folders, and never commit or disclose them; rotate credentials if exposure is suspected.

Risk: Automated market signals and trade suggestions can be wrong or misleading.

Mitigation: Treat analysis as informational guidance, independently verify market data, and apply user-controlled position sizing and loss limits.

Risk: Dependency provenance and runtime safeguards are not sufficient for unattended production trading.

Mitigation: Review locked dependencies and avoid production or unattended trading until enforced confirmations, input validation, and dependency review are in place.

## Reference(s):

- [ApeX Omni API Reference](references/api.md)
- [ApeX Omni API](https://omni.apex.exchange)
- [ApeX Omni Testnet API](https://qa.omni.apex.exchange)
- [CoinGecko Market Chart API](https://api.coingecko.com/api/v3/coins/{coinId}/market_chart)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Private operations require ApeX API credentials and an Omni seed; market data uses ApeX and CoinGecko APIs.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
