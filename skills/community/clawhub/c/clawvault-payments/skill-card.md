## Description:

Security middleware for AI agents handling money. Non-custodial crypto wallets and virtual Visa cards with spending limits, whitelists, and human approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrewszk1](https://clawhub.ai/user/andrewszk1)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to let an agent request crypto payments or virtual card purchases through ClawVault while applying user-defined spending rules and human approval flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can let an agent initiate real crypto transfers or card purchases, including transactions that auto-approve under configured rules.

Mitigation: Configure tight spending limits, recipient or merchant allowlists, and manual approval for higher-risk transactions before use.

Risk: CLAWVAULT_API_KEY is a financial credential.

Mitigation: Store it as a secret, restrict agent access to the minimum required scope, and avoid broad auto-approval rules.

Risk: Temporary card credentials are sensitive and expire quickly.

Mitigation: Use card credentials immediately at checkout and never log, store, or display them beyond the transaction workflow.

## Reference(s):

- [ClawVault Payments on ClawHub](https://clawhub.ai/andrewszk1/skills/clawvault-payments)
- [ClawVault Dashboard](https://clawvault.cc)
- [ClawVault Agent API Keys](https://clawvault.cc/agents)
- [ClawVault Documentation](https://clawvault.cc/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with HTTP and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWVAULT_API_KEY and may involve transaction statuses, approval prompts, and temporary card credentials.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
