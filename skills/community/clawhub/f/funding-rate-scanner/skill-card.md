## Description: <br>
Scan crypto funding rates and find arbitrage opportunities. No API key needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to inspect public Binance Futures funding rates, monitor selected symbols, and produce informational funding-rate analysis for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Funding-rate outputs and annualized return calculations may be stale, volatile, or misleading if used as trading advice. <br>
Mitigation: Treat the output as informational only and verify market data independently before making financial decisions. <br>
Risk: Connecting this informational scanner to exchange-account or trading tools could enable high-risk leveraged crypto trading. <br>
Mitigation: Require explicit human approval before pairing the skill with tools that can place trades or access exchange accounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dagangtj/funding-rate-scanner) <br>
- [Publisher profile](https://clawhub.ai/user/dagangtj) <br>
- [Binance Futures premium index endpoint](https://fapi.binance.com/fapi/v1/premiumIndex) <br>
- [Binance Futures funding rate endpoint](https://fapi.binance.com/fapi/v1/fundingRate) <br>
- [Binance Futures 24hr ticker endpoint](https://fapi.binance.com/fapi/v1/ticker/24hr) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text terminal output with funding-rate rankings, monitored symbols, or single-symbol analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public Binance Futures API responses and does not require an API key.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
