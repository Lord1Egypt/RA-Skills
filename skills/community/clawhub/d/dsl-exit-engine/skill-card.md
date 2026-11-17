## Description:

Guides agents designing or tuning Freqtrade exit logic on Superior Trade by specifying a reusable three-phase exit primitive with an ROI ladder, hard stoploss, and ratcheting trailing stop guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-strategy engineers use this skill to design and tune Freqtrade exit logic for Superior Trade strategies. It helps them compose ROI ladders, hard stoplosses, ratcheting trailing stops, maker-first exits, and parameter-sweep recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backtest claims and default exit parameters may not transfer to a user's market data or live trading environment.

Mitigation: Treat the claims and defaults as starting points, then validate them with local backtests or paper trading before using real funds.

Risk: Maker-first exits can remain unfilled if an implementation lacks a timeout or fallback path.

Mitigation: Configure an exit unfilled timeout or taker fallback when implementing maker-first exit behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/superior-ai/skills/dsl-exit-engine)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with YAML, Python, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides trading-exit design guidance and configuration examples; users should validate defaults on their own market data before live use.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
