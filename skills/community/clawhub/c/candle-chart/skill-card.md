## Description: <br>
Uses akshare stock data and Steve Nison candlestick-pattern logic to generate a dark candlestick chart with signal band and volume view. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wtjjacobj](https://clawhub.ai/user/wtjjacobj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, traders, and analysts use this skill to fetch public A-share daily market data, detect common candlestick patterns, and save a chart for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script fetches public market data through akshare/Tencent for the supplied stock code. <br>
Mitigation: Run it only for stock codes you intend to query through that data source. <br>
Risk: The script creates or overwrites a PNG chart on the user's Desktop named after the stock code. <br>
Mitigation: Check the target filename before running and move or rename any chart you want to preserve. <br>
Risk: Chart pattern labels may be incomplete or misleading if market data is unavailable, delayed, or malformed. <br>
Mitigation: Review the generated chart and source data before using the analysis in downstream decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wtjjacobj/candle-chart) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Analysis] <br>
**Output Format:** [Python script and local PNG chart output with terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public market data through akshare/Tencent and writes a Desktop PNG named after the stock code.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
