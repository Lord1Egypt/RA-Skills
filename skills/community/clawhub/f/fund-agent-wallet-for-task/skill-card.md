## Description: <br>
Fund your CAI custodial wallet so your agent can continue a paid task using create_deposit_link and wallet_balances, with no transfer until the user is ready. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bernardtai](https://clawhub.ai/user/bernardtai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create a CAI hosted deposit link, wait for funding, and re-check wallet balances before an agent continues a paid task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a CAI API key and creates hosted deposit links for wallet funding. <br>
Mitigation: Store the CAI API key in OpenClaw secrets, verify the hosted CAI URL, chain, asset, and payment method before funding, and require separate user approval for any later wallet transfer or purchase. <br>
Risk: Deposit indexing may be partial or delayed, so a balance check may not immediately reflect a completed deposit. <br>
Mitigation: Re-check wallet balances before continuing the paid task and use wallet_deposit_confirm when the user supplies a transaction hash. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bernardtai/fund-agent-wallet-for-task) <br>
- [CAI create_deposit_link reference](https://cai.com/skill.md) <br>
- [CAI developer documentation](https://cai.com/developers.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and hosted action URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CAI hosted deposit links, wallet balance status, and follow-up confirmation guidance.] <br>

## Skill Version(s): <br>
1.0.15 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
