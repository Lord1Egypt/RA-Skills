## Description: <br>
A skill for OpenClaw to research crypto market trends, combine technical and sentiment analysis, and trade ETH on Binance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dymx101](https://clawhub.ai/user/dymx101) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users and developers can use this skill to inspect ETH/USDT market indicators and crypto news sentiment, record an analysis trail, and optionally submit Binance trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Binance trades without a built-in confirmation or spending limit. <br>
Mitigation: Use only a restricted Binance API key with withdrawals disabled, start with dry-run, require explicit approval before every live order, and set external spending and symbol limits. <br>
Risk: Trading and analysis logs may contain private financial records. <br>
Mitigation: Treat generated logs as private records and restrict access to the workspace and log files. <br>


## Reference(s): <br>
- [Clap Trader release page](https://clawhub.ai/dymx101/clap-trader) <br>
- [dymx101 publisher profile](https://clawhub.ai/user/dymx101) <br>
- [Cointelegraph RSS feed](https://cointelegraph.com/rss) <br>
- [CoinDesk RSS feed](https://www.coindesk.com/arc/outboundfeeds/rss/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON analysis outputs, and local log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append analysis notes and trade records to local log files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
