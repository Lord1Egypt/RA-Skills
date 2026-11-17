## Description:

Comprehensive crypto market scanner across Binance, OKX, Bybit, and Bitget with 12 read-only scan types covering arbitrage, market monitoring, and trading signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zadanthony](https://clawhub.ai/user/zadanthony)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use ArbiScan to scan public crypto exchange market data for arbitrage opportunities, anomalies, and trading signals. The skill reports informational results only and does not execute trades or require exchange API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to public crypto exchange APIs.

Mitigation: Install and run it in a virtual environment and expect network access to Binance, OKX, Bybit, and Bitget public API endpoints.

Risk: Market scan results can be mistaken for financial advice or trade instructions.

Mitigation: Treat all results as informational market data and require explicit human review before any trading decision.

Risk: Composing this read-only scanner with trading or executor skills could turn informational findings into trade actions.

Mitigation: Review and approve any trade action separately before combining ArbiScan with exchange trading or executor skills.

Risk: Arbitrage and signal outputs are theoretical and can omit fees, slippage, transfer delays, liquidity, exchange, or regulatory constraints.

Mitigation: Check execution costs, liquidity, transfer timing, counterparty exposure, and compliance requirements before acting on reported opportunities.

Risk: Exchange errors, missing symbols, or rate limits can produce partial results.

Mitigation: Respect the documented request delay and label decisions based on available data as incomplete when some exchanges or symbols are unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zadanthony/skills/arbiscan-skill)
- [Publisher profile](https://clawhub.ai/user/zadanthony)
- [ClawHub](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown tables, plain text tables, or JSON depending on scan mode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only market scan results; standalone CLI supports table, markdown, and JSON output formats.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
