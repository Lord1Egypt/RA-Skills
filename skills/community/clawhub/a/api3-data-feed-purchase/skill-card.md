## Description: <br>
Purchases Api3 data feed subscriptions from market.api3.org. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metobom](https://clawhub.ai/user/metobom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and blockchain operators use this skill to choose an Api3 dAPI, validate the target chain and deviation threshold, inspect provider data, quote subscription cost, execute an on-chain purchase, and optionally read the deployed reader proxy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The purchase flow can use a wallet mnemonic to sign and send a real on-chain transaction. <br>
Mitigation: Use a dedicated low-balance wallet, never a primary wallet mnemonic, and confirm the chain, contract, amount, and gas before approval. <br>
Risk: The skill installs and runs TypeScript dependencies before interacting with blockchain services. <br>
Mitigation: Review the artifact before running, pin dependencies where practical, and consider using an external wallet signer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metobom/skills/api3-data-feed-purchase) <br>
- [Api3 Market](https://market.api3.org) <br>
- [Api3 signed API public endpoint](https://signed-api.api3.org/public/) <br>
- [Api3 data feed pricing data](https://api3dao.github.io/data-feeds/market/dapi-pricing/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with shell commands and transaction summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pnpm, ts-node, and WALLET_MNEMONIC; can initiate an on-chain purchase transaction after user approval.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
