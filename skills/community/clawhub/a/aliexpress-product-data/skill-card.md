## Description:

Search AliExpress, browse a category, pull one product with every SKU variant, read translated buyer reviews, and open a seller's storefront and catalogue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, ecommerce researchers, and market analysts use this skill to search AliExpress, inspect product details and variants, read translated reviews, and review seller catalogue data through Scavio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AliExpress searches and product or seller identifiers are sent to Scavio using the user's API key.

Mitigation: Use the skill only when the user is comfortable sharing those queries and identifiers with Scavio.

Risk: The required SCAVIO_API_KEY could be exposed if placed in source files or logs.

Mitigation: Load the key from the environment or a secret store and keep it out of source control.

Risk: Buyer review text is user-generated and may include personal or subjective content.

Mitigation: Summarize review patterns and avoid profiling individual reviewers.

Risk: API calls consume Scavio credits, including calls that return empty results.

Mitigation: Confirm filters before requesting data and widen filters only when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scavio-ai/skills/aliexpress-product-data)
- [Scavio API documentation](https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=aliexpress-product-data)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=aliexpress-product-data)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses structured JSON returned by Scavio and requires SCAVIO_API_KEY for live calls.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence; artifact frontmatter: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
