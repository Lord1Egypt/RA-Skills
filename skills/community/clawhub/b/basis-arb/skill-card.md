## Description:

Basis Arb provides a Freqtrade strategy template that uses spot-perp basis and funding-rate signals to propose a directional long-perp entry, not a hedged basis arbitrage trade.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and crypto strategy builders use this skill to draft a Hyperliquid/Freqtrade futures strategy that reads spot-perp basis and funding as directional entry signals. It is suited for paper trading, review, and adaptation rather than direct deployment as market-neutral arbitrage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The strategy can be mistaken for market-neutral basis arbitrage even though it only implements the long-perp leg.

Mitigation: Treat outputs as directional futures strategy guidance, and use a separate paired-leg runtime if true hedged arbitrage is required.

Risk: The current backtest evidence reports zero trades because spot OHLCV was unavailable to the Freqtrade engine.

Mitigation: Validate in dry-run mode or with an external basis tracker before committing capital, and confirm that the selected pair has both spot and perp data.

Risk: Crypto futures execution can amplify losses through leverage, margin settings, stale data, and exchange behavior.

Mitigation: Use deliberately limited capital, verify leverage and margin configuration, and independently test funding, basis, stoploss, and timeout behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/superior-ai/skills/basis-arb)
- [Freqtrade informative_pairs documentation](https://www.freqtrade.io/en/stable/strategy-customization/#additional-data-informative_pairs)

## Skill Output:

**Output Type(s):** [markdown, code, configuration, guidance]

**Output Format:** [Markdown with Python and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single strategy template with configuration requirements, tuning notes, variants, and operational caveats.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
