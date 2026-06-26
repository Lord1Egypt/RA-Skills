## Description: <br>
Query blockchain wallet data including balances, DeFi positions, tokens, NFTs, transactions, gas prices, and token approvals across EVM chains via the DeBank API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lolieatapple](https://clawhub.ai/user/lolieatapple) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to query EVM wallet portfolios, DeFi positions, token and NFT holdings, transaction history, approvals, and gas prices through DeBank-backed CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and relies on the external debank-cli npm package. <br>
Mitigation: Install only after accepting trust in the external package and review the package source or provenance according to local policy. <br>
Risk: Wallet queries are sent to DeBank and may expose investigated addresses or query patterns to that service. <br>
Mitigation: Avoid sensitive wallet investigations unless DeBank visibility is acceptable for the intended use. <br>
Risk: A DeBank Pro API key can be stored locally by the CLI. <br>
Mitigation: Use a limited or revocable key where possible and remove it with debank config remove-key when no longer needed. <br>


## Reference(s): <br>
- [DeBank Skill ClawHub Page](https://clawhub.ai/lolieatapple/debank-skill) <br>
- [DeBank Pro API](https://cloud.debank.com/) <br>
- [debank-cli](https://github.com/lolieatapple/debank-cli) <br>
- [debank-skill](https://github.com/lolieatapple/debank-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and summarized query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet balances, token holdings, DeFi positions, NFT holdings, transaction history, approval data, gas prices, and API key setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
