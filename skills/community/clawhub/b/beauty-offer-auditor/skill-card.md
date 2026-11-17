## Description:

Compare and audit two or more beauty or cosmetic offers: cash landed price, bundle split, gift net value, and evidence grade.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bonniegeng-max](https://clawhub.ai/user/bonniegeng-max)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers and buying assistants use this skill to compare beauty or cosmetic offers from links, screenshots, prices, bundles, and gift terms. It supports bounded decision guidance for sale-season, live-stream, duty-free, cross-border, and similar shopping checks without claiming real-time lowest pricing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce stale or incomplete shopping comparisons when offer timing, stock, checkout totals, gift terms, or fulfillment details are missing.

Mitigation: Treat outputs as decision support only and manually confirm the current checkout page, required costs, inventory, seller, invoice, batch, expiry, gift SKU, and return terms before buying.

Risk: Users may expose private shopping or account data while asking for offer comparisons.

Mitigation: Provide only product links, screenshots, prices, and public offer conditions; avoid account pages, addresses, phone numbers, payment details, order data, and other private information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bonniegeng-max/skills/beauty-offer-auditor)
- [Publisher profile](https://clawhub.ai/user/bonniegeng-max)
- [Offer Snapshot v2](references/offer-snapshot-v2.md)
- [Output Template](references/output-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown with structured offer-snapshot fields and evidence-backed comparison tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the user's selected language and region; keeps unknown prices, gift values, and provenance as unknown rather than treating them as zero or confirmed.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact _meta.json says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
