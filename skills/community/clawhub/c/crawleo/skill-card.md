## Description:

Use when OpenClaw needs Crawleo-powered web search, Google Search SERP data, Google Maps place data, URL crawling/content extraction, or headful browser crawling through the Crawleo REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawleo](https://clawhub.ai/user/crawleo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to route agent requests through Crawleo for web search, Google SERP data, Google Maps place lookup, direct URL crawling, and headful browser crawling when simpler crawling is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Crawleo API key could be sent to a caller-chosen server if the client is configured with an unapproved base URL.

Mitigation: Constrain live requests to the approved Crawleo HTTPS origin before production use and review any configuration that changes the request base URL.

Risk: Search terms, URLs, or location queries may contain sensitive or internal information.

Mitigation: Send only non-sensitive inputs to Crawleo and avoid internal, authenticated, or private URLs.

Risk: Headful browser crawling can consume higher Crawleo credits than standard crawling.

Mitigation: Use direct crawling first and reserve headful browser calls for sites that require a headed browser or screenshot workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crawleo/skills/crawleo)
- [Crawleo docs index](https://docs.crawleo.dev/llms.txt)
- [Crawleo REST API introduction](https://docs.crawleo.dev/api-reference/introduction.md)
- [Crawleo authentication](https://docs.crawleo.dev/authentication.md)
- [Crawleo MCP overview](https://docs.crawleo.dev/mcp/overview.md)
- [Crawleo OpenAPI snapshot](https://docs.crawleo.dev/openapi.json)
- [Crawleo search endpoint](https://docs.crawleo.dev/api-reference/endpoint/search.md)
- [Crawleo Google Search endpoint](https://docs.crawleo.dev/api-reference/endpoint/google-search.md)
- [Crawleo Google Maps endpoint](https://docs.crawleo.dev/api-reference/endpoint/google-maps.md)
- [Crawleo crawler endpoint](https://docs.crawleo.dev/api-reference/endpoint/crawler.md)
- [Crawleo headful browser endpoint](https://docs.crawleo.dev/api-reference/endpoint/headful-browser.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript code snippets, shell commands, and API response handling notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live Crawleo calls require CRAWLEO_API_KEY; default tests and examples are intended to be offline-safe unless live execution is explicitly enabled.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
