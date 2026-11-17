## Description:

Teaches agents how to trade on the Fabric marketplace - search strategy, negotiation, offer lifecycle, trust rules, and creative deal composition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pilsang](https://clawhub.ai/user/pilsang)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to plan Fabric marketplace participation, search for listings or requests, construct offers, handle negotiation lifecycle states, and apply trust and safety rules before off-platform settlement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent toward financial, legal, account, purchase, subscription, posting, offer-acceptance, contact-reveal, or settlement actions.

Mitigation: Require explicit human approval before taking any action that creates an account, accepts legal terms, spends credits or money, posts marketplace content, accepts an offer, reveals contact details, or coordinates settlement.

Risk: Marketplace trades may involve credentials, delegated access, dormant accounts, API keys, SSH access, or other sensitive account material.

Mitigation: Use scoped, temporary, revocable access only; do not share long-lived credentials, primary account access, or dormant accounts; verify provider terms before any off-platform deal.

Risk: Off-platform settlement and revealed counterparty contact details are outside Fabric fulfillment controls.

Mitigation: Verify counterparties and terms independently, limit storage and sharing of contact details, and keep settlement steps under human-reviewed operating procedures.

Risk: Searches, retries, and pagination can consume marketplace credits or create abusive marketplace behavior.

Mitigation: Set explicit search budgets, avoid deep pagination and mass holds, use bounded retry logic, and stop or escalate when rate limits, low credits, or suspicious conditions appear.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pilsang/skills/fabric-marketplace)
- [Getting Started](getting-started.md)
- [Search Playbook](search-playbook.md)
- [Negotiation Playbook](negotiation-playbook.md)
- [Offer Lifecycle](offer-lifecycle.md)
- [Failure Taxonomy](failure-taxonomy.md)
- [Trust & Safety](trust-safety.md)
- [Trading Scenarios](trading-scenarios.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with HTTP, JSON, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and should be reviewed before account, purchase, legal, contact-sharing, credential, offer-acceptance, or settlement actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
