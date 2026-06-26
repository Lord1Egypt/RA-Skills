## Description: <br>
Retrieve Aavegotchi NFT data by gotchi ID or name on Base. Returns traits, wearables, rarity scores, kinship, XP, level, and owner data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaigotchi](https://clawhub.ai/user/aaigotchi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, Aavegotchi holders, and analysts use this skill to look up Base-chain Aavegotchi NFT traits, rarity scores, wearables, ownership, kinship, XP, level, and related metadata by token ID or name. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs npm dependencies and runs a local Node script. <br>
Mitigation: Install it only in an environment where local Node scripts and npm dependencies are acceptable, and review the package files before use. <br>
Risk: Gotchi names or IDs are sent to the public Base RPC and Goldsky subgraph by default, or to any configured custom endpoints. <br>
Mitigation: Do not provide wallet private keys or seed phrases, and use trusted custom endpoints if query privacy matters. <br>
Risk: Partial name searches through the subgraph may return a closest match when an exact match is unavailable. <br>
Mitigation: Confirm the returned token ID and name before relying on the lookup result. <br>


## Reference(s): <br>
- [Aavegotchi Data Reference](references/aavegotchi-data.md) <br>
- [Aavegotchi Traits on ClawHub](https://clawhub.ai/aaigotchi/aavegotchi-traits) <br>
- [Base Mainnet RPC](https://mainnet.base.org) <br>
- [Goldsky Aavegotchi Core Base Subgraph](https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-core-base/prod/gn) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Human-readable terminal text plus JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a gotchi ID or name and supports optional environment variables for RPC endpoint, subgraph endpoint, search batch size, retry count, and retry delay.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
