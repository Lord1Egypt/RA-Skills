## Description:

Search Etsy listings, pull one listing with its variations and reviews, open a shop's profile and catalogue, and page through a shop's reviews. 5 endpoints, 2 credits each, structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and ecommerce analysts use this skill to retrieve structured Etsy listing, shop, and review data through Scavio for product research, competitor analysis, price comparison, and agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-directed Etsy lookup requests to Scavio as a third-party provider.

Mitigation: Confirm Scavio is acceptable for the intended data-sharing and operational context before installation.

Risk: The skill requires SCAVIO_API_KEY for API access.

Mitigation: Store the API key in an environment variable or secret manager and avoid committing it to source control or logs.

Risk: Each Etsy lookup spends API credits, including lookups that return empty results.

Mitigation: Confirm the lookup scope before broad searches, monitor credits_used and credits_remaining, and narrow retries when possible.

Risk: Search terms or shop/listing inputs may contain private or unnecessary personal information.

Mitigation: Send only the minimum query, listing, or shop information needed for the task.

Risk: Review text is written by real buyers and may include personal opinions or identifiers.

Mitigation: Summarize review content for product or shop analysis and avoid profiling individual reviewers.

## Reference(s):

- [Scavio Etsy API documentation](https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=etsy-product-data)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=etsy-product-data)
- [ClawHub skill page](https://clawhub.ai/scavio-ai/skills/etsy-product-data)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, structured JSON]

**Output Format:** [Markdown guidance with inline bash and Python examples; API responses are structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY. Etsy endpoints cost 2 credits each and responses include data, response_time, credits_used, and credits_remaining.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
