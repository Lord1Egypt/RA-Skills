## Description:

Trade Polymarket BTC 5-minute and 15-minute fast markets using CEX price momentum signals via Simmer API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richducat](https://clawhub.ai/user/richducat)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to configure, simulate, and run automated Polymarket fast-market trading from crypto momentum signals. It is intended for users who understand prediction-market trading risk and can review strategy settings before live execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can spend real USDC, use wallet credentials, and cancel orders.

Mitigation: Run dry-run first, use an isolated wallet with limited USDC, and avoid sharing broad environment credentials with unrelated tools.

Risk: The advertised minimum-time-between-trades safety control is not enforced.

Mitigation: Do not rely on that setting before live use; enforce cadence externally and review scheduling, budget, and position-size limits.

Risk: The skill depends on simmer-sdk for live trading behavior.

Mitigation: Pin and review simmer-sdk before live use.

Risk: Fast-market positions can resolve before ordinary stop-loss or take-profit monitoring can act.

Mitigation: Size positions conservatively and do not rely on automated stop-losses for 5-minute or 15-minute markets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richducat/skills/dolph-fast-loop)
- [ClawHub publisher profile](https://clawhub.ai/user/richducat)
- [Polymarket CLOB API endpoint](https://clob.polymarket.com)
- [Polymarket Gamma API endpoint](https://gamma-api.polymarket.com/markets)
- [Binance klines API endpoint](https://api.binance.com/api/v3/klines)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown setup guidance with shell commands; CLI text summaries and optional automaton JSON reports during runs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default mode is dry-run; live mode may place Polymarket trades when explicitly enabled.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
