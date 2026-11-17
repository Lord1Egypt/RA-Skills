## Description:

View, create, cancel, bid, and claim Aavegotchi GBM auctions on Base mainnet (8453) using Goldsky subgraph discovery, onchain verification, and Foundry cast execution with DRY_RUN simulation by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinnabarhorse](https://clawhub.ai/user/cinnabarhorse)

### License/Terms of Use:


## Use Case:

External developers and operators use this skill to inspect and manage Aavegotchi GBM auctions on Base mainnet, including auction creation, cancellation, bidding, swap-assisted bidding, and claims. It is intended for workflows that need subgraph discovery, immediate onchain verification, and explicit simulation before any transaction broadcast.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private keys may be exposed or misused when passed to command-line transaction broadcasts.

Mitigation: Use only a dedicated, low-balance wallet; avoid primary or treasury keys; prefer a hardware wallet, keystore, or external signer; and keep DRY_RUN enabled until broadcast is explicitly required.

Risk: Auction state can change between discovery and execution, causing stale bids, failed claims, or unintended transactions.

Mitigation: Refetch auction data immediately before execution and verify current onchain highestBid, token contract, token id, quantity, timing, claimed, and cancelled state before simulation or broadcast.

Risk: Untrusted auction or user-provided values can lead to unsafe shell command construction.

Mitigation: Validate addresses as 0x-prefixed 40-character hex strings, validate integer inputs as base-10 digits, avoid eval or shell re-execution, and substitute only checked literal values into command examples.

## Reference(s):

- [Aavegotchi GBM Skill on ClawHub](https://clawhub.ai/cinnabarhorse/skills/aavegotchi-gbm-skill)
- [Skill homepage](https://github.com/aavegotchi/aavegotchi-gbm-skill)
- [Addresses / Constants](artifact/references/addresses.md)
- [Bid Math](artifact/references/bid-math.md)
- [Common Recipes](artifact/references/recipes.md)
- [Subgraph Queries](artifact/references/subgraph.md)
- [Swap Amount Math](artifact/references/swap-math.md)
- [GBM Auction Presets](artifact/references/presets.md)
- [Logs / Event Scans](artifact/references/logs.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, Python, and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes transaction simulation guidance, environment variable setup, subgraph queries, and Foundry cast commands.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
