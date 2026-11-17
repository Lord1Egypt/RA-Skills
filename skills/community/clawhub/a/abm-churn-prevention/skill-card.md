## Description:

Helps agents advise on SaaS churn prevention through cancel-flow design, save offers, churn-risk signals, and failed-payment recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariokarras](https://clawhub.ai/user/mariokarras)

### License/Terms of Use:

MIT-0

## Use Case:

External SaaS product, growth, and customer success teams use this skill to plan churn-reduction work, including voluntary cancellation flows, save-offer design, proactive retention, and dunning/payment-recovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cancellation-flow or billing-provider changes may affect real customer accounts or legal compliance.

Mitigation: Review proposed cancellation, billing, CRM, email, and analytics changes with appropriate business and legal owners before applying them to production systems.

Risk: Recommendations can be miscalibrated when churn, product-usage, cancellation-reason, or payment-failure data is incomplete.

Mitigation: Ground rollout decisions in product-specific metrics, exit-survey data, payment-failure data, and controlled tests before making material offer or cancellation-flow changes.

Risk: Retention and dunning experiences can harm users if they obscure cancellation, overuse discounts, or apply inappropriate urgency.

Mitigation: Keep cancellation paths visible, match save offers to stated cancellation reasons, use clear payment consequences, and avoid guilt-trip copy.

## Reference(s):

- [Cancel Flow Patterns](artifact/references/cancel-flow-patterns.md)
- [Dunning Playbook](artifact/references/dunning-playbook.md)
- [ClawHub Skill Page](https://clawhub.ai/mariokarras/skills/abm-churn-prevention)

## Skill Output:

**Output Type(s):** [guidance, markdown, text, configuration]

**Output Format:** [Markdown guidance with tables, examples, and implementation recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code is included in the artifact; outputs may propose billing, CRM, email, or analytics changes that require human approval.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
