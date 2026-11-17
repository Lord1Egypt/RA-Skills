## Description:

Fetches structured public web data through Crawlora's hosted REST API, including search, bounded crawls, and durable research jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve public-web prices, listings, reviews, transcripts, search results, trends, financial data, and places for research and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, URLs, locations, and request bodies are sent to Crawlora's hosted API.

Mitigation: Send only public-web inputs that the user is comfortable sharing with Crawlora.

Risk: Successful requests consume credits, and crawl or research jobs may continue running.

Mitigation: Agree on source scope and credit limits before starting jobs; cancel jobs when no longer needed.

Risk: An exposed API key can permit unauthorized requests and spending.

Mitigation: Keep CRAWLORA_API_KEY private; never include it in responses or commit it.

## Reference(s):

- [Crawlora skill on ClawHub](https://clawhub.ai/crawlora-org/skills/crawlora)
- [Crawlora endpoint catalog](reference/catalog.md)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown with optional JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public-web results may be paginated; research and crawl jobs can continue after the initial request.]

## Skill Version(s):

1.0.43 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
