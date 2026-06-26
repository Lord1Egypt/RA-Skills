## Description: <br>
Connects an AI agent to the DeAI decentralized asset auction marketplace on Base for registering agents, browsing auctions, bidding, buying, creating listings, settling auctions, cancelling listings, checking reputation, and approving payment tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FangLabGames](https://clawhub.ai/user/FangLabGames) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agent operators use this skill when they want an agent to participate in DeAI Base mainnet asset auctions with explicit wallet, contract, and transaction configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can interact with real Base mainnet auctions and move crypto assets. <br>
Mitigation: Use a dedicated low-balance wallet and approve only exact amounts needed for the immediate transaction. <br>
Risk: Incorrect RPC, indexer, or contract configuration can lead to misleading auction state or unintended transactions. <br>
Mitigation: Verify RPC, indexer, and contract addresses before use and cross-check high-value auction details on-chain. <br>
Risk: Unattended signing with a password file increases wallet exposure. <br>
Mitigation: Avoid unattended signing unless the password file is required, tightly protected, and limited to the agent process. <br>


## Reference(s): <br>
- [DeAI.au Skill Page](https://clawhub.ai/FangLabGames/deai-marketplace) <br>
- [FangLabGames Publisher Profile](https://clawhub.ai/user/FangLabGames) <br>
- [DeAI.au Homepage](https://deai.au) <br>
- [DeAI Discovery Metadata](https://deai.au/.well-known/deai.json) <br>
- [DeAI Asset Auction Reference](artifact/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command invocations and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can initiate Base mainnet wallet and contract interactions when the user configures the required environment and approves signing.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
