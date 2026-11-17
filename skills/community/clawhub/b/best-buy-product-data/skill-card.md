## Description:

Search Best Buy listings, products, deals, reviews, and store availability through Scavio, with results returned as structured product data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can search Best Buy US products and categories, compare prices and open-box offers, inspect specifications and customer reviews, and check deals, store hours, and pickup availability.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: ZIP codes and product queries are sent to Scavio when checking store availability or retrieving product data.

Mitigation: Use only ZIP codes and queries you are comfortable sharing with Scavio.

Risk: The security evidence reports a benign verdict with medium confidence and a partial scanner review.

Mitigation: Review the unresolved path-like reference and the skill behavior before installation.

Risk: The SCAVIO_API_KEY authenticates requests to a credit-based API.

Mitigation: Keep the key in an environment variable or secret store and out of prompts and source code.

## Reference(s):

- [Scavio Best Buy product API documentation](https://scavio.dev/docs/bestbuy-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data)
- [Scavio Best Buy API overview](https://scavio.dev/bestbuy-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data)
- [ClawHub release page](https://clawhub.ai/scavio-ai/skills/best-buy-product-data)

## Skill Output:

**Output Type(s):** [JSON, API calls, Guidance]

**Output Format:** [Structured JSON product data with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live Best Buy US data; available fields vary by endpoint.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
