## Description: <br>
Crypto market analysis using Asrai API. Covers technical analysis, screeners, sentiment, forecasting, smart money, Elliott Wave, cashflow, DEX data, and AI-powered insights. Each API call costs $0.005 USDC from your own wallet on Base mainnet via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abuzerasr](https://clawhub.ai/user/abuzerasr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request paid crypto market analysis, trading signals, sentiment, forecasts, DEX data, portfolio references, and live exchange position summaries through Asrai MCP tools or bash commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a wallet private key for paid x402 calls and documents remote URL forms that can expose a key in query parameters. <br>
Mitigation: Use a dedicated low-balance wallet, avoid putting a primary private key in URLs or shared env files, avoid remote URLs containing key=0x..., and set a low ASRAI_MAX_SPEND. <br>
Risk: The positions workflow can use exchange API credentials for MEXC, Binance, or Lighter. <br>
Mitigation: Use only read-only, IP-restricted exchange keys with trading and withdrawals disabled. <br>
Risk: The skill can make repeated paid API calls from the user's wallet. <br>
Mitigation: Tell users when paid analysis is being requested, prefer the minimum useful set of calls, and keep a low session spend cap. <br>
Risk: The skill provides crypto trading signals, forecasts, portfolio references, and buy or avoid guidance that could influence financial decisions. <br>
Mitigation: Present outputs as analysis rather than guaranteed outcomes, preserve uncertainty, and encourage users to verify with independent sources before trading. <br>


## Reference(s): <br>
- [Asrai x402 Endpoints](artifact/references/endpoints.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/abuzerasr/asrai-x402) <br>
- [Asrai Agents Website](https://asrai.me/agents) <br>
- [asrai-mcp npm Package](https://www.npmjs.com/package/asrai-mcp) <br>
- [x402 Protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with optional inline shell commands and MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses paid x402 API calls signed from the user's Base mainnet wallet; some tools require exchange API credentials.] <br>

## Skill Version(s): <br>
2.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
