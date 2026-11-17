## Description:

Use when writing a symmetric Bollinger-band mean-reversion strategy on the 4h timeframe, with long-or-short entries on 2-sigma band touches, RSI confirmation, ADX-gated range regimes, and a tight ROI ladder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-strategy authors use this skill to draft or adapt a Freqtrade-style 4h Bollinger Band mean-reversion strategy for liquid crypto majors. It provides strategy logic, parameter ranges, reference configuration, backtest framing, and deployment cautions for range-bound market regimes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides speculative trading guidance, and its quoted backtest results are not guarantees of future performance.

Mitigation: Validate the strategy independently, run dry-run or paper-trading tests first, and treat backtest metrics as historical evidence only.

Risk: Futures trading, leverage, stop execution, and slippage can cause rapid losses or liquidation.

Mitigation: Use conservative position sizing, isolated margin where applicable, hard stops, and avoid deployment around major news or scheduled macro events unless risk is explicitly accepted.

Risk: The strategy can lose when range-bound markets transition into strong trends or when applied to meme or low-liquidity pairs.

Mitigation: Restrict use to liquid majors, monitor ADX/regime behavior, and avoid extending the strategy to pairs outside the validated profile without fresh testing.

## Reference(s):

- [Bollinger Reverter 4h on ClawHub](https://clawhub.ai/superior-ai/skills/bollinger-reverter-4h)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with Python and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces trading-strategy guidance and example configuration; users should validate with dry-run or paper trading before use.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
