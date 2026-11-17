## Description:

Helps agents advise SaaS teams on reducing voluntary and involuntary churn through cancellation flows, save offers, payment recovery, and retention strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrhuang09](https://clawhub.ai/user/mrhuang09)

### License/Terms of Use:


## Use Case:

Product, growth, and engineering teams use this skill to design or improve SaaS cancellation flows, dunning sequences, save offers, churn measurement, and retention interventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce business or product guidance for cancellation, billing, payment recovery, and customer data workflows that is mistaken for legal advice.

Mitigation: Review recommendations against applicable subscription, cancellation, billing, privacy, and marketing rules before deployment.

Risk: The skill may suggest changes that affect live billing, account state, cancellation, payment retries, or customer communications.

Mitigation: Require explicit user approval and implementation review before applying live billing or account changes.

Risk: The skill may ask an agent to read local product-marketing context to tailor churn recommendations.

Mitigation: Limit shared context to relevant product information and avoid exposing unnecessary customer or payment data.

## Reference(s):

- [Churn Prevention on ClawHub](https://clawhub.ai/mrhuang09/skills/churn-prevention-2)
- [Cancel Flow Patterns](artifact/references/cancel-flow-patterns.md)
- [Dunning Playbook](artifact/references/dunning-playbook.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands]

**Output Format:** [Markdown guidance with tables, checklists, templates, and occasional inline shell command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend billing, analytics, and retention workflow changes that should be reviewed before implementation.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact metadata version 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
