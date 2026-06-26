## Description: <br>
View, add, and execute Aavegotchi Baazaar listings on Base mainnet (8453), buying with GHST directly or USDC via swapAndBuy* with dry-run-first safety controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinnabarhorse](https://clawhub.ai/user/cinnabarhorse) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent users use this skill to inspect, add, simulate, and, after explicit confirmation, execute Aavegotchi Baazaar marketplace listings on Base mainnet. It supports GHST purchases, USDC swap-and-buy flows, listing setup, approvals, and deterministic transaction-argument checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare and broadcast real marketplace transactions that spend assets or create listings. <br>
Mitigation: Keep DRY_RUN enabled until the transaction summary has been reviewed, and require DRY_RUN=0 plus BROADCAST_CONFIRM=CONFIRM_SEND before any cast send broadcast. <br>
Risk: A private key is required for broadcasts and could expose funds if copied into chat or logs. <br>
Mitigation: Read PRIVATE_KEY only from the environment, never print it, and use a dedicated low-balance wallet. <br>
Risk: Wrong-chain, wrong-wallet, stale-listing, or approval mistakes can cause failed or unintended transactions. <br>
Mitigation: Verify Base chain ID 8453, confirm the private key matches FROM_ADDRESS, refetch listings immediately before simulation or broadcast, and revoke unused token or NFT approvals. <br>
Risk: Untrusted listing values or user-provided strings could lead to unsafe shell command construction. <br>
Mitigation: Use only allowlisted command templates, validate addresses and integer arguments before substitution, quote data values, and reject free-form shell execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cinnabarhorse/aavegotchi-baazaar) <br>
- [Addresses / Constants](artifact/references/addresses.md) <br>
- [Category Maps](artifact/references/categories.md) <br>
- [Common Recipes](artifact/references/recipes.md) <br>
- [Subgraph Queries](artifact/references/subgraph.md) <br>
- [USDC swapAmount Math](artifact/references/usdc-swap-math.md) <br>
- [Goldsky Aavegotchi Core Base subgraph](https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-core-base/prod/gn) <br>
- [CoinGecko GHST/USD price endpoint](https://api.coingecko.com/api/v3/simple/price?ids=aavegotchi&vs_currencies=usd) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash, GraphQL, and Python command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run transaction simulation is the default; real broadcasts require environment-gated confirmation and user review of transaction details.] <br>

## Skill Version(s): <br>
0.1.4 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
