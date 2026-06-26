## Description: <br>
ButterSwap helps agents retrieve Butter Network cross-chain swap quotes, routes, and transaction payloads across supported blockchain networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IvanMacaron](https://clawhub.ai/user/IvanMacaron) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use ButterSwap to inspect supported chains and tokens, compare cross-chain swap routes, and assemble swap transaction payloads for user review before signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Swap routes or transaction payloads may include incorrect token, chain, fee, slippage, approval, receiver, refund, contract target, calldata, or native value details. <br>
Mitigation: Use the skill for quotes and transaction construction, then independently verify all wallet and transaction details before signing. <br>
Risk: Swap intent and wallet-address details are sent to Butter Router. <br>
Mitigation: Install and use only when this third-party API data sharing is acceptable. <br>


## Reference(s): <br>
- [ButterSwap ClawHub release](https://clawhub.ai/IvanMacaron/butter-swap-skill) <br>
- [Butter API Docs](https://docs.butternetwork.io/butter-swap-integration/integration-guide) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with API request examples and JSON transaction data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include route options, token metadata, chain IDs, fees, slippage settings, contract target, calldata, native value, and transaction chain ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
