## Description: <br>
Calculates multi-timeframe Binance Event Contract signal suggestions for BTCUSDT and ETHUSDT, including entries, targets, stop loss, confidence, and position sizing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[acwxpunh](https://clawhub.ai/user/acwxpunh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users monitoring Binance Event Contract cycles use this skill to combine K-line, liquidity, ICT structure, and risk inputs into structured BTCUSDT/ETHUSDT signal suggestions for speculative analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Signal outputs could influence risky speculative trading decisions. <br>
Mitigation: Independently verify entries, stops, targets, confidence, and position sizes; do not treat outputs as financial advice or instructions to trade. <br>
Risk: The skill uses a disclosed market-data API key. <br>
Mitigation: Use a least-privilege or read-only market-data API key and avoid granting trading or withdrawal permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/acwxpunh/binance-event-contract-signal) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style structured trading signal text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes direction, entry zone, targets, stop loss, confidence, cycle type, position size, and a Signal Pending fallback when inputs are insufficient.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
