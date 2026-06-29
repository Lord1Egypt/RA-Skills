## Description: <br>
Basis Arb helps agents draft a Freqtrade strategy template that reads spot-perp basis and funding as a directional long-perp signal, not a hedged arbitrage bot. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[superior-ai](https://clawhub.ai/user/superior-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading-strategy builders use this skill to create or adapt a Freqtrade template for Hyperliquid spot-perp basis signals and to understand the limits before paper trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The strategy is financial trading guidance and is not a guaranteed arbitrage bot. <br>
Mitigation: Use dry-run or paper trading first and compare entries against an external basis tracker before any live deployment. <br>
Risk: The template uses futures cross-margin configuration and exchange credentials. <br>
Mitigation: Review margin settings and credential handling carefully before connecting it to a live exchange account. <br>
Risk: The signal depends on both spot and perpetual market data for the same asset. <br>
Mitigation: Confirm the exchange pair has both spot and perpetual data available; otherwise the strategy may produce no trades. <br>


## Reference(s): <br>
- [Basis Arb on ClawHub](https://clawhub.ai/superior-ai/basis-arb) <br>
- [Freqtrade informative_pairs documentation](https://www.freqtrade.io/en/stable/strategy-customization/#additional-data-informative_pairs) <br>
- [Superior Trade alpha scan improvement plan](https://github.com/Superior-Trade/superior-turborepo/blob/main/docs/alpha-scan-improvement-plan.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with Python and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes financial-risk caveats and expects user review before live trading.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact frontmatter lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
