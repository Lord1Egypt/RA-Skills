## Description: <br>
Query and analyze on-chain data via MCP tools and CLI commands across Solana, BSC, and Ethereum for token analytics, market ranking, wallet profiling, and WebSocket streaming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harry5556](https://clawhub.ai/user/harry5556) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run live on-chain data queries, screen token risk signals, inspect wallet PnL and holdings, monitor market trends, and stream crypto trade data. It is intended for ChainStream MCP, CLI, SDK, and API workflows that may require authentication, quota checks, or user-approved payment steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide wallet creation, private-key import, payment, and transaction-signing workflows. <br>
Mitigation: Require explicit user approval before wallet creation, private-key import, payment, or transaction-signing steps, and prefer read-only API-key or MCP access for analytics. <br>
Risk: The skill connects to live third-party crypto services and may incur quota usage or purchases. <br>
Mitigation: Check authentication and subscription status first, present available plans clearly, and never auto-select or auto-purchase a plan. <br>


## Reference(s): <br>
- [ChainStream skill page](https://clawhub.ai/harry5556/chainstream-data) <br>
- [ChainStream documentation](https://docs.chainstream.io) <br>
- [ChainStream dashboard](https://app.chainstream.io) <br>
- [ChainStream CLI README](https://github.com/chainstream-io/cli) <br>
- [API endpoints](references/api-endpoints.md) <br>
- [API schema](references/api-schema.md) <br>
- [Market discovery](references/market-discovery.md) <br>
- [Query examples](references/query-examples.md) <br>
- [Token research](references/token-research.md) <br>
- [Wallet profiling](references/wallet-profiling.md) <br>
- [WebSocket streams](references/websocket-streams.md) <br>
- [x402 wallet authentication](references/x402-auth.md) <br>
- [Authentication](shared/authentication.md) <br>
- [Payment protocols](shared/x402-payment.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live API, MCP, CLI, SDK, and WebSocket query patterns; payment, wallet, and private-key workflows require explicit user approval.] <br>

## Skill Version(s): <br>
3.1.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
