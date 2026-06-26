## Description: <br>
Trade Polymarket 5-minute crypto fast markets using Binance 1-minute candle body analysis, volume surge detection, and direction alignment across BTC, ETH, SOL, XRP, and BNB. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mibayy](https://clawhub.ai/user/Mibayy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and agent operators use this skill to run or adapt a Polymarket fast-market trading workflow that evaluates Binance candle structure, selects the strongest eligible crypto signal, and can either dry-run or place live trades through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades and create financial loss. <br>
Mitigation: Start in dry-run or paper mode, then confirm the exact market, pair, amount, daily limits, stop-loss or drawdown settings, and the explicit live flag before enabling real trades. <br>
Risk: Overbroad trading credentials could expose funds beyond the intended strategy. <br>
Mitigation: Use only keys scoped to trading and never use credentials with withdrawal access. <br>
Risk: A valid signal may still be unsuitable because of slippage, weak edge, or a rapidly changing market. <br>
Mitigation: Review the skill's context checks and keep conservative position sizing and thresholds before running scheduled live cycles. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mibayy/candle-momentum) <br>
- [Binance Klines API endpoint](https://api.binance.com/api/v3/klines) <br>
- [Simmer API base](https://api.simmer.markets) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance, Python CLI output, and JSON-like run results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run is the default; live trading requires SIMMER_API_KEY and an explicit --live flag.] <br>

## Skill Version(s): <br>
2.0.1 (source: server evidence, SKILL.md frontmatter, clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
