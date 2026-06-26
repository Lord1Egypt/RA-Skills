## Description: <br>
View, create, cancel, bid, and claim Aavegotchi GBM auctions on Base mainnet (8453), using Goldsky subgraph discovery with onchain verification and Foundry cast execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinnabarhorse](https://clawhub.ai/user/cinnabarhorse) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Web3 operators use this skill to inspect and operate Aavegotchi GBM auction flows on Base mainnet, including auction creation, cancellation, bidding, swap-backed bidding, and claiming. The skill emphasizes subgraph lookup, onchain revalidation, and dry-run simulation before any broadcast. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare and, when explicitly authorized, broadcast real Base mainnet transactions using a private key. <br>
Mitigation: Use a dedicated low-balance wallet, keep DRY_RUN=1 by default, and only set DRY_RUN=0 after reviewing the exact transaction details. <br>
Risk: Auction state may change between discovery and execution, causing stale bids or incorrect transaction assumptions. <br>
Mitigation: Refetch subgraph data and verify contract state onchain immediately before any simulation or broadcast. <br>
Risk: Token approvals and swap-backed bids can expose funds if addresses, allowances, or slippage settings are wrong. <br>
Mitigation: Verify contract addresses and auction parameters, avoid broad approvals unless understood, and use conservative slippage and allowance settings. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cinnabarhorse/aavegotchi-gbm-skill) <br>
- [Addresses / Constants (Base Mainnet)](artifact/references/addresses.md) <br>
- [Bid Math (Minimum Next Bid)](artifact/references/bid-math.md) <br>
- [Logs / Event Scans](artifact/references/logs.md) <br>
- [GBM Auction Presets](artifact/references/presets.md) <br>
- [Common Recipes (Foundry cast + Subgraph)](artifact/references/recipes.md) <br>
- [Subgraph Queries (Base GBM Auctions)](artifact/references/subgraph.md) <br>
- [Swap Amount Math (USDC / ETH -> GHST)](artifact/references/swap-math.md) <br>
- [Base Mainnet RPC](https://mainnet.base.org) <br>
- [Aavegotchi GBM Goldsky Subgraph](https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-gbm-baazaar-base/prod/gn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash, curl, Python, and Foundry cast command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires cast, curl, python3, Base mainnet RPC access, wallet environment variables, and optional Goldsky API credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
