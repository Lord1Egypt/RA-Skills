## Description:

This skill lets an AI agent complete flight booking payments through a CAI custodial wallet after the user confirms the payee and amount.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bernardtai](https://clawhub.ai/user/bernardtai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent complete the payment step for a held flight itinerary after explicit confirmation of recipient, amount, chain, and token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move real funds through a CAI wallet after user confirmation.

Mitigation: Use a CAI key with pay-only scope when possible, keep wallet balances limited, and verify recipient, amount, chain, and token before approving any transfer.

Risk: A payment sent to an incorrect recipient, chain, token, or amount may be irreversible.

Mitigation: Require explicit user confirmation of the full recipient, amount, chain, and token before executing a transfer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bernardtai/skills/book-flight-with-agent)
- [CAI full contract](https://cai.com/skill.md)
- [CAI agent payment workflow](https://cai.com/skill-references/agent-payment-workflow.md)
- [CAI agent card](https://cai.com/.well-known/agent.json)
- [CAI developer documentation](https://cai.com/developers.html)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline shell commands and payment workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CAI_API_KEY with pay or full scope; payment transfers should occur only after user confirmation.]

## Skill Version(s):

1.0.15 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
