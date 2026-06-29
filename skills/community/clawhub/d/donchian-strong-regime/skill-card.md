## Description: <br>
Helps agents draft a Freqtrade/Superior Trade trend-breakdown short strategy gated by EMA separation, ADX, and recent downside momentum, with sample Python strategy code and reference configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superior-ai](https://clawhub.ai/user/superior-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-strategy authors use this skill to produce a regime-gated short strategy, including entry and exit logic, tunable parameters, Python strategy code, and reference configuration for BTC/USDC:USDC-style futures testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reported backtest is based on only 6 trades, so the 100% win rate may not generalize. <br>
Mitigation: Independently backtest on longer and out-of-sample data before using the strategy for live trading. <br>
Risk: Using the strategy with real funds can expose users to cryptocurrency futures losses. <br>
Mitigation: Start with dry-run testing, explicit risk limits, and small isolated allocations before considering live deployment. <br>
Risk: Low-liquidity assets can create unreliable Donchian lows from liquidation wicks. <br>
Mitigation: Restrict testing and deployment to deeply liquid major pairs unless separate liquidity validation supports broader use. <br>
Risk: Loosening the regime gate can change the intended behavior and increase exposure to sideways-market noise. <br>
Mitigation: Preserve the triple-confirmation gate unless new validation data supports a parameter change. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/superior-ai/donchian-strong-regime) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown containing prose, Python code, and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes trading assumptions, backtest summary, tunable parameter ranges, known failure modes, and deployment guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
