## Description: <br>
Generates informational crypto price-signal and DeFi-yield summaries from public market data, with text or JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drivenautoplex1](https://clawhub.ai/user/drivenautoplex1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch public crypto market and DeFi yield data and produce informational trading-signal summaries for selected assets. Outputs should not be treated as financial advice or validated trading probabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives actionable trading guidance and the security summary says its stated trading-analysis capabilities are materially overstated. <br>
Mitigation: Treat outputs as rough informational signals only, not financial advice, and verify conclusions against independent market analysis before acting. <br>
Risk: Advertised confidence intervals, backtests, regime detection, and whale-flow analysis may not be validated by the implementation. <br>
Mitigation: Do not rely on those probabilities or historical-performance claims unless the implementation is updated and independently verified. <br>
Risk: The skill uses a CoinGecko API key and installs unpinned dependencies. <br>
Mitigation: Use a limited CoinGecko key, review dependency versions before installation, and run the skill in a constrained environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drivenautoplex1/dfw-trading-signals) <br>
- [Publisher profile](https://clawhub.ai/user/drivenautoplex1) <br>
- [Project homepage from metadata](https://github.com/drivenautoplex1/openclaw-skills) <br>
- [CoinGecko API endpoint](https://api.coingecko.com/api/v3) <br>
- [DeFiLlama yield pools endpoint](https://yields.llama.fi/pools) <br>
- [SaucerSwap pools endpoint](https://api.saucerswap.finance/pools) <br>
- [Binance klines endpoint](https://api.binance.com/api/v3/klines) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text report or JSON object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Network-dependent market data output; requires review before use in trading decisions.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
