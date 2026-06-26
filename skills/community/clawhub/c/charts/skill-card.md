## Description: <br>
Generate 90-day candlestick technical-analysis charts with SMA 20/50, RSI, Fibonacci retracements, and pattern detection for BTC, ETH, XRP, SUI, gold, and silver. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryandeangraves](https://clawhub.ai/user/ryandeangraves) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and market-analysis users use this skill to generate local chart image files and concise technical-analysis output for a fixed set of crypto and precious-metal assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs the agent to send generated chart files to a fixed Telegram recipient. <br>
Mitigation: Review the local charting module before use and remove or change the hardcoded Telegram target unless the user explicitly wants charts sent to that recipient. <br>
Risk: The chart workflow relies on market-data requests to Yahoo Finance or CoinGecko. <br>
Mitigation: Use the skill only when outbound market-data requests are acceptable for the user's environment and task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryandeangraves/charts) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks; generated PNG chart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local market-charting code and may request market data from Yahoo Finance or CoinGecko.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
