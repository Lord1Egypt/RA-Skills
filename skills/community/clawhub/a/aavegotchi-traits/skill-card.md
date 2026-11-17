## Description:

Retrieve Aavegotchi NFT data by gotchi ID or name on Base. Returns traits, wearables, rarity scores, kinship, XP, level, and owner data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaigotchi](https://clawhub.ai/user/aaigotchi)

### License/Terms of Use:


## Use Case:

Developers and external Aavegotchi users use this skill to look up Base-chain Aavegotchi NFT traits, rarity scores, wearables, ownership, staking, kinship, XP, and level by token ID or name.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs npm packages and relies on the ethers/ws dependency chain.

Mitigation: Use deterministic installs such as npm ci and consider updating dependencies before deployment.

Risk: The skill makes public network requests to Base RPC and Goldsky using the supplied gotchi ID or name.

Mitigation: Use public or non-sensitive endpoints unless you understand what an endpoint logs.

Risk: Name lookup can return a closest subgraph match when an exact match is unavailable.

Mitigation: Confirm the returned token ID and name before relying on lookup results.

## Reference(s):

- [Aavegotchi Data Reference](references/aavegotchi-data.md)
- [Aavegotchi Traits on ClawHub](https://clawhub.ai/aaigotchi/skills/aavegotchi-traits)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Human-readable terminal text followed by structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Looks up one Aavegotchi identifier per run and may use public Base RPC and Goldsky subgraph requests.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
