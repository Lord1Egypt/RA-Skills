## Description: <br>
Agent completes the checkout/payment step of a workflow using CAI wallet balances, user confirmation, transfer status, and on-chain proof. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bernardtai](https://clawhub.ai/user/bernardtai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to let an agent finish checkout after a cart or quote is ready. The workflow checks CAI wallet balances, creates a deposit link if needed, asks the user to confirm payment details, and completes a transfer with status or activity proof. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support real checkout or payment transfers using a CAI wallet and API key. <br>
Mitigation: Install only when real checkout support is intended, keep CAI_API_KEY secret, and require personal verification of merchant or payee, amount, chain, token, and final line items before approving any transfer. <br>
Risk: Arbitrary merchant card iframe checkout is outside the primary CAI payment path. <br>
Mitigation: Prefer on-chain or custodial @cai.com payment paths and use marketplace-specific flows where the workflow requires them. <br>


## Reference(s): <br>
- [CAI canonical skill](https://cai.com/skill.md) <br>
- [CAI agent payment workflow](https://cai.com/skill-references/agent-payment-workflow.md) <br>
- [CAI agent payment](https://cai.com/agent-payment.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with task steps, inline tool names, and a setup command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CAI_API_KEY and user confirmation before transfers.] <br>

## Skill Version(s): <br>
1.0.15 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
