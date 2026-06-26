## Description: <br>
Agentsmint helps agents create and manage NFT collections on Base by minting NFTs, launching collections, listing items for sale, checking portfolios, deploying contracts, lazy minting, and tracking editions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kit-the-fox](https://clawhub.ai/user/kit-the-fox) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agents use this skill to create NFT collections, list NFTs, retrieve mint instructions, confirm purchases, and inspect portfolio-related collection data on Base through AgentsMint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide costly or irreversible blockchain and marketplace actions such as deploy, mint, buy, list, confirm, and ownership transfer. <br>
Mitigation: Require separate confirmation before each such action, showing the exact wallet, chain, contract, recipient, listing or collection ID, price, gas estimate, transaction hash, and ownership setting. <br>
Risk: Using a primary wallet could expose more funds than needed for NFT management on Base. <br>
Mitigation: Use a dedicated low-balance wallet for AgentsMint activity. <br>


## Reference(s): <br>
- [AgentsMint API Base](https://www.agentsmint.com/api/v1) <br>
- [AgentsMint BitBuddies Collection](https://agentsmint.com/bitbuddies) <br>
- [ClawHub Skill Page](https://clawhub.ai/kit-the-fox/agentsmint) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and REST API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet, chain, listing, collection, price, gas, transaction hash, and ownership-transfer values that should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
