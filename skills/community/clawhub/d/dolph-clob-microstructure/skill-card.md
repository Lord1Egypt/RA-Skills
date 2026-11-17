## Description:

Analyzes Polymarket CLOB order book microstructure to find structural inefficiencies, score liquidity gaps, imbalance, whale activity, and fake breakout patterns, and generate trading signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richducat](https://clawhub.ai/user/richducat)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-agent operators use this skill to scan active Polymarket markets, evaluate order-book microstructure, and produce actionable signals for dry-run or live Simmer trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real prediction-market trades while the security summary reports weak safety controls for the requested financial authority.

Mitigation: Review carefully before installing, prefer dry-run mode, and use live mode only with a constrained Simmer account and conservative per-trade, per-run, and daily limits.

Risk: The artifact can continue when safety context is unavailable.

Mitigation: Prefer a version or wrapper that fails closed when market context, slippage, or edge checks cannot be retrieved.

Risk: Dependency or external API changes could alter trading behavior.

Mitigation: Pin dependencies and validate behavior against the Polymarket and Simmer APIs before enabling scheduled live execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/richducat/skills/dolph-clob-microstructure)
- [Publisher Profile](https://clawhub.ai/user/richducat)
- [Polymarket CLOB Book API](https://clob.polymarket.com/book)
- [Polymarket Trades API](https://data-api.polymarket.com/trades)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and CLI/log text with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces market scores, trading-signal labels, dry-run summaries, and optional live order placement through SimmerClient.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact files declare 2.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
