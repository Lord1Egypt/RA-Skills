## Description:

Operate Aavegotchi Gotchiverse player workflows on Base mainnet (8453): alchemica channeling, surveying and harvesting, crafting installations/tiles, building on parcels, installation upgrades, craft/upgrade queue management, and parcel access-right management through subgraph-first discovery and Foundry cast verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinnabarhorse](https://clawhub.ai/user/cinnabarhorse)

### License/Terms of Use:


## Use Case:

External Aavegotchi Gotchiverse players and agent operators use this skill to prepare, simulate, and execute player-level Realm, Installation, Tile, and access-right workflows on Base mainnet. It is intended for wallet-controlled gameplay operations that require careful transaction review before broadcast.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a raw wallet private key and includes live blockchain transaction commands.

Mitigation: Use a dedicated low-value wallet, keystore, hardware wallet, or isolated signer, and avoid passing a production private key directly with --private-key.

Risk: Broadcasting incorrect transactions can change parcel state, access rights, queues, or token balances on Base mainnet.

Mitigation: Keep DRY_RUN as a review posture, simulate with cast call, verify chain ID 8453, contract addresses, parcel IDs, access-right settings, and costs, and broadcast only after explicit approval.

Risk: Subgraph data or user-provided values can be stale, malformed, or unsafe for shell substitution.

Mitigation: Refetch subgraph state before state-changing steps, revalidate critical values onchain, accept only validated address and uint formats, and avoid eval or shell re-entry with untrusted values.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cinnabarhorse/skills/aavegotchi-gotchiverse)
- [Addresses / Constants](references/addresses.md)
- [Subgraph Queries](references/subgraph.md)
- [Realm Recipes](references/realm-recipes.md)
- [Installation Recipes](references/installation-recipes.md)
- [Tile Recipes](references/tile-recipes.md)
- [Parcel Access Rights](references/access-rights.md)
- [Common Failure Modes and Fixes](references/failure-modes.md)
- [Gotchiverse Base Subgraph](https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/gotchiverse-base/prod/gn)
- [Aavegotchi Core Base Subgraph](https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-core-base/prod/gn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash, cast, curl, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces transaction preparation, simulation, broadcast, troubleshooting, and setup guidance; it does not itself custody keys or execute commands without the host agent/user running them.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
