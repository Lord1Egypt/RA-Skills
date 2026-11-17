## Description:

Query and analyze on-chain token, market, wallet, and WebSocket data through ChainStream MCP, CLI, SDK, and API workflows across Solana, BSC, and Ethereum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harry5556](https://clawhub.ai/user/harry5556)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and AI agents use Chainstream Data to retrieve and interpret on-chain token, market, wallet, and streaming data, including token security checks, holder analysis, market discovery, wallet profiling, and subscription-aware access setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill combines read-oriented blockchain analytics with wallet setup, persistent authentication, private-key import paths, and real crypto payment flows.

Mitigation: Prefer API-key or preconfigured MCP access for read-only analytics; avoid importing production private keys and use a low-balance wallet if payment flows are needed.

Risk: CLI or protocol setup can involve unpinned command execution and external installers.

Mitigation: Review commands before execution and independently verify installer sources before running shell installer pipelines.

Risk: Wallet signing, subscription purchases, webhook changes, or transaction-related actions can alter external systems or spend funds.

Mitigation: Require explicit user confirmation before signing, purchasing, modifying webhooks, or performing transaction-related actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harry5556/skills/chainstream-data)
- [ChainStream MCP server](https://mcp.chainstream.io/mcp)
- [ChainStream API base URL](https://api.chainstream.io)
- [ChainStream dashboard](https://app.chainstream.io)
- [API Schema Reference](artifact/references/api-schema.md)
- [ChainStream Data API Endpoints](artifact/references/api-endpoints.md)
- [Token Research Reference](artifact/references/token-research.md)
- [Market Discovery Reference](artifact/references/market-discovery.md)
- [Wallet Profiling Reference](artifact/references/wallet-profiling.md)
- [WebSocket Streams Reference](artifact/references/websocket-streams.md)
- [x402 Wallet Authentication](artifact/references/x402-auth.md)
- [Payment Protocols](artifact/shared/x402-payment.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and API or MCP usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live data query guidance, machine-readable command output expectations, and safety checks before payment, signing, or webhook actions.]

## Skill Version(s):

3.1.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
