## Description:

Agent completes the checkout/payment step of a workflow using CAI wallet balances, user confirmation, and transfer with on-chain proof.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bernardtai](https://clawhub.ai/user/bernardtai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill when an agent has prepared an order, cart, or quote and needs help completing payment through CAI wallet balance checks, funding, confirmation, transfer, and proof lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide wallet-based checkout and transfer workflows involving financial value.

Mitigation: Require explicit user confirmation of payee, amount, chain, and token before any transfer.

Risk: A vague purchase request could route the user into CAI payment behavior unintentionally.

Mitigation: Use the skill only when the user clearly wants CAI involved in the checkout or payment step.

Risk: Merchant card iframe payment paths may not be supported by the CAI tools described in the artifact.

Mitigation: Prefer the documented on-chain and custodial @cai.com payment paths, and handle marketplace-specific flows separately.

## Reference(s):

- [CAI Skill Reference](https://cai.com/skill.md)
- [Agent Payment Workflow](https://cai.com/skill-references/agent-payment-workflow.md)
- [CAI Agent Payment](https://cai.com/agent-payment.html)
- [ClawHub skill page](https://clawhub.ai/bernardtai/skills/agent-checkout-completion)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and tool-oriented instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include payment confirmation details, funding setup guidance, transfer status checks, and on-chain proof references.]

## Skill Version(s):

1.0.15 (source: evidence metadata and release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
