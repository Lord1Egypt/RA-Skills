## Description: <br>
Purchases API3 data feed subscriptions from market.api3.org. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metobom](https://clawhub.ai/user/metobom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and blockchain operators use this skill to discover API3 dAPIs and supported chains, quote subscription pricing, purchase a selected data feed subscription on-chain, and optionally read the resulting feed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses WALLET_MNEMONIC from a local .env file to sign blockchain transactions. <br>
Mitigation: Use only a dedicated low-balance wallet and never paste a main wallet seed phrase into chat or project files. <br>
Risk: The purchase flow can spend funds and broadcast an irreversible on-chain transaction. <br>
Mitigation: Verify the feed, chain, deviation threshold, and quoted price carefully, and require explicit user approval before running the purchase command. <br>


## Reference(s): <br>
- [API3 Market](https://market.api3.org) <br>
- [ClawHub Skill Page](https://clawhub.ai/metobom/api3-data-feed-purchase) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and summary tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides package installation, feed and chain validation, price quoting, transaction execution, and optional feed reading.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
