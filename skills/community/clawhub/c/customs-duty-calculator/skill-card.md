## Description:

Estimate import duties, tariffs, and landed costs for cross-border ecommerce shipments by HS code and destination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers and operations teams use this skill to estimate per-SKU landed cost, compare DDP and DDU shipping choices, and investigate unexpected customs duty bills across export markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Duty, VAT/GST, de minimis, surcharge, and tariff rules can change, and estimates may become stale or jurisdiction-specific.

Mitigation: Verify current rates and thresholds with official customs sources or a customs broker before relying on estimates for pricing or compliance.

Risk: Incorrect HS classification, customs valuation, or preferential-origin assumptions can materially change landed cost and compliance obligations.

Mitigation: Document classification logic, valuation method, origin evidence, and consider binding rulings for high-value or high-volume shipments.

## Reference(s):

- [HS Code Guide](references/hs-code-guide.md)
- [DDP vs DDU Tradeoffs](references/incoterm-tradeoffs.md)
- [De Minimis and Threshold Quick Reference](references/de-minimis-table.md)
- [Landed Cost Output Template](references/output-template.md)
- [Duty Estimate Quality Checklist](assets/quality-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown worksheet with tables, calculations, assumptions, and checklist items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimates depend on user-provided product, HS code, valuation, origin, destination, currency, Incoterm, and current duty or tax rates.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
