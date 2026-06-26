## Description: <br>
Fetches cryptocurrency token prices and generates candlestick charts using CoinGecko or Hyperliquid market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redf426](https://clawhub.ai/user/redf426) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users can request current crypto prices, recent price movement, and candlestick chart images for supported tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token symbols and chart durations are sent to disclosed public market-data APIs. <br>
Mitigation: Use the skill only when this API sharing is acceptable for the requested token lookup. <br>
Risk: The skill creates temporary chart image files that may remain if cleanup is skipped. <br>
Mitigation: Delete only the generated crypto_chart files returned by the script after sending or using the chart. <br>
Risk: Unusual token names or shell metacharacters could cause unsafe command usage around the script. <br>
Mitigation: Pass ordinary token symbols and durations, and avoid shell metacharacters in user-provided token names. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/redf426/crypto-chart) <br>
- [CoinGecko API](https://api.coingecko.com/api/v3/) <br>
- [Hyperliquid Info API](https://api.hyperliquid.xyz/info) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, image files, shell commands] <br>
**Output Format:** [JSON response with formatted text and an optional PNG candlestick chart path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and matplotlib; uses temporary cache and chart files under /tmp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
