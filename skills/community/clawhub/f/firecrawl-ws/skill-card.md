## Description:

AI-native web scraping, crawling, domain mapping, and structured extraction. Use for converting websites into LLM-ready Markdown, scraping pages with dynamic JS/actions, crawling full domains, or extracting schema-based structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI engineers, data engineers, and agent builders use this skill to guide Firecrawl scraping, crawling, URL mapping, and schema-based extraction workflows for authorized websites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad scraping, crawling, and browser actions against websites.

Mitigation: Use it only for sites the operator is authorized to scrape, set explicit crawl limits, and avoid logged-in, internal, personal, or sensitive pages without approval.

Risk: Target URLs and retrieved page content may be sent to Firecrawl.

Mitigation: Review data sensitivity before use and avoid sending confidential or regulated content to external services unless approved.

Risk: The self-hosting example can expose an unauthenticated API if deployed publicly as written.

Mitigation: Enable authentication, bind privately or place the API behind an authenticated proxy, pin container images or digests, and set conservative CPU, memory, and crawl limits.

## Reference(s):

- [Firecrawl API Reference & SDK Guides](references/api_reference.md)
- [Firecrawl Self-Hosting Reference Guide](references/self_hosting.md)
- [Firecrawl GitHub Repository](https://github.com/firecrawl/firecrawl)
- [Firecrawl Advanced Scraping Guide](https://docs.firecrawl.dev/advanced-scraping-guide)
- [Firecrawl Agent Endpoint](https://docs.firecrawl.dev/features/agent)
- [Firecrawl Rate Limits](https://docs.firecrawl.dev/rate-limits)
- [Firecrawl Self-Hosting Guide](https://raw.githubusercontent.com/firecrawl/firecrawl/main/SELF_HOST.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with API examples, SDK snippets, Docker Compose configuration, and JSON schema examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include guidance for Firecrawl API calls that return Markdown, HTML, screenshots, links, images, or structured JSON.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
