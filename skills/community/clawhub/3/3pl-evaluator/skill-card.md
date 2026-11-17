## Description:

Systematically evaluate and compare third-party logistics (3PL) fulfillment partners against your order volume, product characteristics, and growth stage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators and advisors use this skill to shortlist, compare, audit, or renegotiate third-party logistics providers using normalized cost, service, technology, fit, and contract criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rate cards, contracts, order profiles, and reference-call notes may contain sensitive business information.

Mitigation: Handle inputs as sensitive business data and avoid exposing provider pricing, customer volume, or contract details beyond the evaluation context.

Risk: The recommendation can be misleading when vendor claims, pricing, SLAs, or assumptions are incomplete or stale.

Mitigation: Verify current written pricing, contract terms, demos, and reference checks before acting, and disclose incomplete data as assumptions.

Risk: Comparing providers on headline fees can understate total fulfillment cost.

Mitigation: Normalize each candidate to landed cost per order, including receiving, storage, pick and pack, packaging, shipping, returns, technology fees, minimums, and peak surcharges.

## Reference(s):

- [3PL Evaluation Output Template](references/output-template.md)
- [Evaluation Scorecard Guide](references/evaluation-scorecard-guide.md)
- [3PL Fee Glossary & Pricing Models](references/fee-glossary-and-pricing-models.md)
- [3PL Evaluation Quality Checklist](assets/3pl-evaluation-checklist.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown with scorecards, landed-cost tables, assumptions, red flags, negotiation levers, and transition planning guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided operational data, candidate quotes, contracts, and reference notes; incomplete inputs should be disclosed as assumptions.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
