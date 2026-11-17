## Description:

View, add, and execute Aavegotchi Baazaar listings on Base mainnet (8453), buying with GHST directly or with USDC through swapAndBuy while defaulting to dry-run simulation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinnabarhorse](https://clawhub.ai/user/cinnabarhorse)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect Aavegotchi Baazaar listings, prepare marketplace transactions, simulate purchases or listings, and broadcast only after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Marketplace and approval commands can affect crypto assets if broadcast with an unintended signer, chain, contract, spender, or amount.

Mitigation: Use a wallet limited to funds you are willing to risk, keep DRY_RUN enabled by default, and manually verify chain, signer, token or NFT contract, spender, amount, and confirmation gates before any approval or broadcast.

Risk: setApprovalForAll grants collection-wide operator authority until revoked.

Mitigation: Run collection-wide approvals only after manual review of the NFT contract and operator address, and revoke approval when it is no longer needed.

Risk: Listings can be cancelled, sold, or price-updated between lookup and transaction execution.

Mitigation: Refetch listing data immediately before simulation or broadcast, then re-simulate if any transaction argument changes.

## Reference(s):

- [Aavegotchi Baazaar ClawHub page](https://clawhub.ai/cinnabarhorse/skills/aavegotchi-baazaar)
- [Addresses / Constants](references/addresses.md)
- [Category Maps](references/categories.md)
- [Common Recipes](references/recipes.md)
- [Subgraph Queries](references/subgraph.md)
- [USDC swapAmount Math](references/usdc-swap-math.md)
- [Base mainnet RPC](https://mainnet.base.org)
- [Aavegotchi Core Base Goldsky subgraph](https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-core-base/prod/gn)
- [CoinGecko GHST/USD simple price API](https://api.coingecko.com/api/v3/simple/price?ids=aavegotchi&vs_currencies=usd)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash, GraphQL, and Python command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run transaction simulation is the default; real broadcasts require explicit environment and confirmation gates.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
