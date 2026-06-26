## Description: <br>
Access CoinMarketCap data via x402 pay-per-request protocol with USDC payments on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bryan-cmc](https://clawhub.ai/user/bryan-cmc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agent builders use this skill to integrate CoinMarketCap market data through x402 paid REST and MCP access without managing a traditional API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic x402 payment flows can spend USDC when an agent or MCP client makes paid requests without clear per-request controls. <br>
Mitigation: Require explicit confirmation or an external budget limit before any agent or MCP client can make paid x402 requests. <br>
Risk: Wallet private keys and funded accounts are required for the payment flow. <br>
Mitigation: Use a fresh low-balance hot wallet for Base USDC payments and never use a main wallet private key. <br>
Risk: The quick-start flow depends on npm packages used to sign and submit payments. <br>
Mitigation: Pin and review npm dependencies before installation or deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bryan-cmc/cmc-x402) <br>
- [ClawHub Homepage Metadata](https://github.com/coinmarketcap/skills-for-ai-agents-by-CoinMarketCap) <br>
- [x402 Endpoint Reference](references/endpoints.md) <br>
- [x402 Payment Details](references/payment-details.md) <br>
- [x402 Documentation](https://docs.x402.org) <br>
- [x402 Protocol](https://x402.org) <br>
- [x402 GitHub](https://github.com/coinbase/x402) <br>
- [CoinMarketCap API Documentation](https://coinmarketcap.com/api/documentation) <br>
- [CoinMarketCap x402 MCP Endpoint](https://mcp.coinmarketcap.com/x402/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript, bash, JSON, and endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include paid x402 REST or MCP request guidance that requires wallet, Base USDC, and explicit spending controls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
