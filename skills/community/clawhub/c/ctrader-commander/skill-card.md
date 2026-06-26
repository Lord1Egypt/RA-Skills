## Description: <br>
Place and manage cTrader orders, check open positions, fetch live quotes and OHLC candles, and query account balance and equity through a local HTTP proxy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elmoyeldo](https://clawhub.ai/user/elmoyeldo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Traders and developers use this skill to ask an agent for cTrader account checks, quote and candle retrieval, and order-management command guidance against a locally running cTrader proxy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to issue commands to a local proxy that can act on a credentialed cTrader account. <br>
Mitigation: Use a demo or restricted account first, keep the proxy bound to trusted local access only, stop it when not supervised, and require manual confirmation before any order, close, cancel, account switch, or generic command. <br>
Risk: Trading commands may use broker-specific symbol IDs and unit-based volumes, which can cause unintended instruments or position sizes if copied incorrectly. <br>
Mitigation: Look up the symbol ID for the active broker and account before market data or order requests, and verify volume in units before submitting any trading command. <br>
Risk: The local proxy loads credentials from its server environment, so callers do not need to supply a token at command time. <br>
Mitigation: Review and pin the external proxy code before use, restrict access to the running proxy, and supervise the proxy whenever it is available to an agent. <br>


## Reference(s): <br>
- [cTrader OpenAPI Proxy homepage](https://github.com/LogicalSapien/ctrader-openapi-proxy) <br>
- [Endpoint reference](artifact/endpoints.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for a local proxy at localhost:9009 and may include trading order, account, quote, candle, close-position, cancel-order, and account-switch commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
