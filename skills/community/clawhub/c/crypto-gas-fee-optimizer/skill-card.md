## Description:

Checks live gas prices across Ethereum, Base, Arbitrum, Optimism, and Polygon, estimates USD transaction costs, and ranks chains to help users choose a lower-cost chain or timing window before sending on-chain transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

External users, crypto traders, DeFi users, and smart contract deployers use this skill to compare current gas costs across supported EVM chains before bridging, swapping, claiming, deploying contracts, or batching transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gas estimates and timing notes are informational and may not match the final cost of a specific signed transaction.

Mitigation: Confirm live wallet or node estimates before signing, especially for high-value or time-sensitive transactions.

Risk: Public RPC providers and CoinGecko can rate-limit, return errors, or be temporarily unavailable.

Mitigation: Treat missing chain results as incomplete data and retry or compare against another trusted gas source before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssidharhubble/skills/crypto-gas-fee-optimizer)
- [CoinGecko simple price endpoint](https://api.coingecko.com/api/v3/simple/price?ids=ethereum,matic-network&vs_currencies=usd)
- [Ethereum PublicNode RPC endpoint](https://ethereum-rpc.publicnode.com)
- [Base PublicNode RPC endpoint](https://base-rpc.publicnode.com)
- [Arbitrum PublicNode RPC endpoint](https://arbitrum-one-rpc.publicnode.com)
- [Optimism PublicNode RPC endpoint](https://optimism-rpc.publicnode.com)
- [Polygon PublicNode RPC endpoint](https://polygon-bor-rpc.publicnode.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Terminal table or JSON, with concise explanatory guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sorted cheapest-first by estimated transaction cost when pricing data is available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
