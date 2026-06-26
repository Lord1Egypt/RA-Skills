## Description: <br>
Access Alchemy's multi-chain APIs for tokens, NFTs, transfers, prices, portfolios, simulations, webhooks, Solana, and JSON-RPC via API key or the x402 Agentic Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sahilaujla](https://clawhub.ai/user/sahilaujla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to integrate Alchemy blockchain infrastructure, choose the right API endpoint, and draft requests for multi-chain data, webhooks, simulations, Solana, and JSON-RPC workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet private-key handling and x402 payment flows can expose funds if credentials are pasted into chat, stored in source files, or reused with high balances. <br>
Mitigation: Prefer an Alchemy API key or a testnet or dedicated low-balance wallet, keep private keys out of chat and source files, and require manual approval for every payment. <br>
Risk: Generated requests may broadcast transactions, change webhook state, or spend USDC through automatic payment flows. <br>
Mitigation: Review each generated command before execution, test on testnets where possible, and require explicit approval for transaction broadcasts, payments, and webhook changes. <br>


## Reference(s): <br>
- [Alchemy Official Skill Page](https://clawhub.ai/sahilaujla/alchemy-official) <br>
- [Alchemy Developer Docs](https://www.alchemy.com/docs) <br>
- [Alchemy Dashboard](https://dashboard.alchemy.com) <br>
- [Node JSON-RPC](references/node-json-rpc.md) <br>
- [NFT API](references/data-nft-api.md) <br>
- [Portfolio APIs](references/data-portfolio-apis.md) <br>
- [Prices API](references/data-prices-api.md) <br>
- [Token API](references/data-token-api.md) <br>
- [Transfers API](references/data-transfers-api.md) <br>
- [Webhooks Overview](references/webhooks-overview.md) <br>
- [Solana Overview](references/solana-overview.md) <br>
- [Agentic Gateway](AGENTIC-GATEWAY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [Markdown with inline curl, TypeScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference API keys, SIWE tokens, x402 payments, wallet setup, webhook configuration, and network-specific endpoint limits.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
