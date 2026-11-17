## Description:

Get instructions for funding an Agnic wallet with USDC, including wallet address lookup, Base network transfer guidance, and balance verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need agent guidance for adding USDC to an Agnic wallet on Base, checking authentication, retrieving the wallet address, and verifying the resulting balance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports a financial workflow through a mutable CLI package reference.

Mitigation: Prefer a pinned, reviewed Agnic CLI version before using the commands for wallet funding.

Risk: Credential handling guidance can expose tokens if tokens are passed on the command line or included in chats or logs.

Mitigation: Use AGNIC_TOKEN through a protected environment and keep tokens out of command history, chats, and logs.

Risk: Sending USDC to an unverified or incorrect wallet address can result in loss of funds.

Mitigation: Verify the wallet address through an independent trusted Agnic channel before sending USDC.

## Reference(s):

- [Agnic Dashboard](https://app.agnic.ai)
- [Base Bridge](https://bridge.base.org)
- [ClawHub Skill Page](https://clawhub.ai/agnicpay-prog/skills/agnicpay-fund-wallet)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet funding steps, authentication notes, network warnings, and balance verification commands.]

## Skill Version(s):

2.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
