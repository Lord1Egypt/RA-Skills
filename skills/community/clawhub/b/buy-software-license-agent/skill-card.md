## Description:

Agent buys SaaS or software licenses on your behalf using CAI custodial wallet after you confirm payee and amount.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bernardtai](https://clawhub.ai/user/bernardtai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill when an agent needs to prepare a software or SaaS license purchase or renewal through a CAI custodial wallet, with transfer only after explicit user confirmation of payment details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financially sensitive payment workflow could result in unintended transfer if payment details are not verified.

Mitigation: Before approving any transfer, verify the vendor, destination, amount, chain, token, and intended license or subscription.

Risk: Overbroad or mishandled CAI_API_KEY permissions could expose payment capabilities beyond the intended task.

Mitigation: Store CAI_API_KEY as a secret and prefer the narrowest CAI_API_KEY permissions available for the purchase workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bernardtai/skills/buy-software-license-agent)
- [CAI skill reference](https://cai.com/skill.md)
- [Agent payment workflow](https://cai.com/skill-references/agent-payment-workflow.md)
- [CAI developers](https://cai.com/developers.html)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and ordered workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CAI_API_KEY for payment-capable CAI wallet workflows.]

## Skill Version(s):

1.0.15 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
