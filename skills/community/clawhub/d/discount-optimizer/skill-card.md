## Description:

Calculate optimal discount levels based on unit cost, conversion targets, and inventory velocity so promos move product without destroying margin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators use this skill to size discounts from contribution margin, break-even volume lift, promo mechanic fit, and inventory velocity before launching a sale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive product costs, margins, and sales velocity data may be exposed if shared in an untrusted agent environment.

Mitigation: Use the skill only in trusted environments and redact or aggregate confidential figures when possible.

Risk: Discount recommendations can be misleading if inputs omit fees, commissions, offer stacking, returns, or inventory constraints.

Mitigation: Review each generated promotion manually against current platform terms, margin floors, and launch guardrails before publishing.

## Reference(s):

- [Discount Optimizer on ClawHub](https://clawhub.ai/leooooooow/skills/discount-optimizer)
- [Output Template](references/output-template.md)
- [Margin Math Guide](references/margin-math-guide.md)
- [Promo Mechanics Guide](references/promo-mechanics-guide.md)
- [Quality Checklist](assets/quality-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown discount plan with tables, calculations, guardrails, and monitoring checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided product economics; calculations are decision support and should be manually reviewed before launch.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
