## Description: <br>
Fetch real-time prices, 24-hour statistics, K-line charts, and market information for Binance spot trading pairs using the Binance API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[torchesfrms](https://clawhub.ai/user/torchesfrms) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Binance spot market data for trading pairs, including current prices, 24-hour movement, candlestick data, and basic token market details. <br>

### Deployment Geography for Use: <br>
Global, subject to Binance API availability, local rules, and Binance terms. <br>

## Known Risks and Mitigations: <br>
Risk: Market-data requests may be routed through a configured HTTP proxy, exposing requested symbols and API traffic metadata to the proxy operator. <br>
Mitigation: Use only a proxy you control or trust, and verify that proxy use complies with local rules and Binance terms before running the scripts. <br>
Risk: Binance API access may be unavailable or restricted in some regions. <br>
Mitigation: Confirm Binance API availability and applicable terms for the intended location before relying on the skill. <br>


## Reference(s): <br>
- [Binance Spot API](https://api.binance.com/api/v3) <br>
- [ClawHub Skill Page](https://clawhub.ai/torchesfrms/binance-exchange) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command output in plain text or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to Binance market-data endpoints and may use a user-configured HTTP proxy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
