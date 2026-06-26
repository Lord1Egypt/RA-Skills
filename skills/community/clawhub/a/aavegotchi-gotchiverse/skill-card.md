## Description: <br>
Operate Aavegotchi Gotchiverse player workflows on Base mainnet (8453), including alchemica channeling, surveying and harvesting, crafting installations and tiles, parcel building, installation upgrades, craft and upgrade queue management, and parcel access-right management through subgraph-first discovery and onchain verification with Foundry cast. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinnabarhorse](https://clawhub.ai/user/cinnabarhorse) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to prepare and execute Aavegotchi Gotchiverse player operations on Base mainnet. It helps agents discover parcel and Gotchi state, validate contract data, simulate transactions, and provide Foundry cast commands for approved broadcasts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real Base mainnet transactions can move assets or change parcel state. <br>
Mitigation: Use a dedicated low-balance wallet, keep DRY_RUN enabled until ready, simulate first, and approve each cast send transaction deliberately. <br>
Risk: Using the wrong network, contract address, or sender key can cause failed or unintended transactions. <br>
Mitigation: Verify chain ID 8453, contract addresses, and PRIVATE_KEY-to-FROM_ADDRESS alignment immediately before broadcast. <br>
Risk: PRIVATE_KEY exposure can compromise the wallet. <br>
Mitigation: Do not print or log PRIVATE_KEY, avoid shell history exposure, and supply secrets only through controlled environment variables. <br>
Risk: Untrusted user or subgraph values could produce unsafe shell commands. <br>
Mitigation: Validate addresses and uint values before substitution, keep placeholders quoted, and avoid eval, bash -c, or sh -c with user-controlled values. <br>


## Reference(s): <br>
- [Aavegotchi Gotchiverse ClawHub release](https://clawhub.ai/cinnabarhorse/aavegotchi-gotchiverse) <br>
- [Parcel Access Rights](artifact/references/access-rights.md) <br>
- [Addresses / Constants (Base Mainnet)](artifact/references/addresses.md) <br>
- [Common Failure Modes and Fixes](artifact/references/failure-modes.md) <br>
- [Installation Recipes (Foundry cast)](artifact/references/installation-recipes.md) <br>
- [Realm Recipes (Foundry cast)](artifact/references/realm-recipes.md) <br>
- [Subgraph Queries (Base)](artifact/references/subgraph.md) <br>
- [Tile Recipes (Foundry cast)](artifact/references/tile-recipes.md) <br>
- [Base Mainnet RPC endpoint](https://mainnet.base.org) <br>
- [Gotchiverse Base subgraph endpoint](https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/gotchiverse-base/prod/gn) <br>
- [Aavegotchi Core Base subgraph endpoint](https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-core-base/prod/gn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and Foundry cast command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run-first transaction guidance; requires user-supplied wallet, RPC, contract, token, and subgraph environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
