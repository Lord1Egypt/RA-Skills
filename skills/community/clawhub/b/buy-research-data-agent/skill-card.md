## Description:

Agent purchases paid datasets, API credits, or research reports using CAI wallet after user confirmation. Fund via create_deposit_link if needed. Powered by CAI.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bernardtai](https://clawhub.ai/user/bernardtai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and research agents use this skill to purchase paid datasets, API credits, or research reports through CAI wallet workflows after explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A payment transfer may be irreversible or sent to the wrong recipient, amount, or purchase target.

Mitigation: Before confirming any transfer, verify the dataset or report, recipient, amount, refund terms, and irreversible-payment warning.

Risk: The agent may not have complete paywall or checkout details for an arbitrary research purchase.

Mitigation: Require the agent to surface product, price, payment method, payee details, and hosted checkout limitations before preparing payment.

## Reference(s):

- [CAI Skill Reference](https://cai.com/skill.md)
- [CAI Agent Payment](https://cai.com/agent-payment.html)
- [CAI Developers](https://cai.com/developers.html)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before transfer and can include wallet activity or transfer status as payment proof.]

## Skill Version(s):

1.0.15 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
