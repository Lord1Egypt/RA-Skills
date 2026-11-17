## Description:

Funds a CAI custodial wallet through hosted deposit links so an agent can continue a paid task, with balance checks before any transfer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bernardtai](https://clawhub.ai/user/bernardtai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate a CAI hosted deposit link, wait for funding, re-check wallet balances, and continue a paid parent task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user could provide a CAI API key or open a hosted deposit link without intending to fund the agent wallet.

Mitigation: Confirm wallet-funding intent first and only provide a CAI API key acceptable for this purpose.

Risk: A downstream payment task could proceed before the hosted deposit is reflected in wallet balance.

Mitigation: Review deposit links and balances, then re-check wallet_balances before any transfer.

Risk: Deposit indexing may be partial_live after funding.

Mitigation: Use wallet_deposit_confirm when the user supplies a transaction hash.

## Reference(s):

- [CAI Skill Reference: create_deposit_link](https://cai.com/skill.md)
- [CAI Developers](https://cai.com/developers.html)
- [ClawHub Skill Page](https://clawhub.ai/bernardtai/skills/fund-agent-wallet-for-task)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CAI hosted action URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes hosted deposit URLs when generated; the agent waits for funding and re-checks balances before any transfer.]

## Skill Version(s):

1.0.15 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
