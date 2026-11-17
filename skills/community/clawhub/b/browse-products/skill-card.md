## Description:

Semantic product search API using vector embeddings. Search products by natural language queries with price filtering, pagination, and relevance scoring. Use when the user wants to search products, browse a product catalog, or find items by description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gzipped](https://clawhub.ai/user/gzipped)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search a product catalog with natural language queries, optional price filters, pagination, and relevance scoring, then present matching products with prices, images, and store links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product search queries are sent to the documented external API.

Mitigation: Avoid including secrets, account details, or sensitive personal information in search terms.

Risk: Search results can include outbound or affiliate store links.

Mitigation: Review destination links before acting on them and present store links clearly to users.

## Reference(s):

- [Products Browse Skill API Reference](artifact/reference.md)
- [ClawHub skill page](https://clawhub.ai/gzipped/skills/browse-products)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown]

**Output Format:** [Markdown guidance with HTTP and cURL examples; API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search queries are sent to an external product search API; query text is limited to 500 characters, page size to 100 results, and bulk search to 50 queries per request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
