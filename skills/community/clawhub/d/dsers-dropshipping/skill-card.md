## Description:

Helps dropshipping sellers assess product profitability, resolve supplier and order issues, prepare store listings, and check stores against relevant platform and consumer rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dsers](https://clawhub.ai/user/dsers)

### License/Terms of Use:

MIT-0

## Use Case:

External dropshipping sellers use this skill to review profitability and pricing, handle supplier or order problems, improve product listings, and check a store before launch or advertising. It can work from information the seller provides, and can use live supplier data or save products, prices, and pricing rules when DSers MCP is connected.

### Deployment Geography for Use:

Global, with specific guidance for the US, EU, and UK

## Known Risks and Mitigations:

Risk: The scan verdict is benign, but it is not a guarantee; binary image files were outside some static analyzers’ scope.

Mitigation: Review the supplied image assets and decide whether the product-listing and live-store workflows fit the intended use before installing.

Risk: Connected DSers workflows can save products, prices, or pricing rules to the user's account.

Mitigation: Show the exact account changes and wait for the user's agreement before making them.

Risk: Consumer rules, platform policies, and fees vary by market and can change.

Mitigation: Confirm the applicable current rule or fee through its official source and use the seller's own figures before advising or calculating.

## Reference(s):

- [Profit and pricing guidance](artifact/references/profit.md)
- [Supplier and order guidance](artifact/references/suppliers.md)
- [Product listing guidance](artifact/references/listing.md)
- [Store launch guidance](artifact/references/launch.md)
- [Rules and official sources](artifact/references/rules.md)
- [Connecting DSers MCP](artifact/references/connect-dsers.md)
- [DSers](https://www.dsers.com)
- [DSers MCP skill connection](https://ai.dsers.com/mcp/clawhub-skill)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, CSV data]

**Output Format:** [Markdown text, calculations, customer message drafts, product listing copy, or Shopify CSV content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses seller-provided figures unless live DSers data is available; labels estimates and assumptions.]

## Skill Version(s):

0.1.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
