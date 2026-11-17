## Description:

Searches 1688 products by text, image, or product link, finds same or similar items, and supports purchase comparison with price, sales, supplier, and product attribute filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External users and purchasing-focused agents use this skill to search 1688 for products, same-item matches, similar products, and lower-cost or higher-volume supplier options. It is intended for product discovery and comparison, not order placement, payment, logistics tracking, or inventory management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable 1688 AK or OAuth credentials may be exposed in chat, command output, or local files.

Mitigation: Use an isolated environment, avoid pasting real AK values into chat, avoid status commands that reveal live credentials until redaction is fixed, and rotate any AK that appears in transcripts or logs.

Risk: The skill requires access to a 1688 AK for product search and comparison.

Mitigation: Install only when granting this credential access is acceptable, and clear or rotate credentials when the skill is no longer needed.

Risk: Product recommendations, prices, links, and supplier details are only as reliable as the API response returned at execution time.

Mitigation: Do not invent missing product details, present returned links and fields as evidence, and ask the user to retry or reconfigure credentials when the CLI reports API or authentication errors.

## Reference(s):

- [1688 Product Find on ClawHub](https://clawhub.ai/1688aiinfra/skills/1688-product-find)
- [Publisher profile: 1688aiinfra](https://clawhub.ai/user/1688aiinfra)
- [Text search capability](references/capabilities/text_search.md)
- [Image search capability](references/capabilities/image_search.md)
- [Link search capability](references/capabilities/link_search.md)
- [Compare capability](references/capabilities/compare.md)
- [Configure capability](references/capabilities/configure.md)
- [Error handling](references/common/error-handling.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON containing a success flag, markdown product tables or errors, and structured product data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product results include item identifiers, titles, image URLs, detail URLs, price, SKU, supplier, sales, stock, promotion tags, service tags, and selling points when returned by the 1688 API.]

## Skill Version(s):

1.7.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
