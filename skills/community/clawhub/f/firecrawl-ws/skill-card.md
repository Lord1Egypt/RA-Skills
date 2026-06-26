## Description: <br>
AI-native web scraping, crawling, domain mapping, and structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, AI engineers, agent builders, data engineers, and web scraping engineers use this skill to guide Firecrawl-based scraping, crawling, URL mapping, and structured extraction workflows for LLM-ready web content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Firecrawl requests may share target URLs, prompts, extraction schemas, and scraped page content with Firecrawl unless the service is self-hosted. <br>
Mitigation: Do not submit secrets, authenticated pages, or internal-only URLs without authorization; use approved public sources or a protected self-hosted deployment for sensitive work. <br>
Risk: The self-hosting example can expose the API broadly and disable authentication if copied without changes. <br>
Mitigation: Bind self-hosted services to localhost or a private network, enable authentication, and place the API behind a protected reverse proxy before use. <br>


## Reference(s): <br>
- [Firecrawl skill page](https://clawhub.ai/simonpierreboucher02/firecrawl-ws) <br>
- [API Reference & SDK Guides](references/api_reference.md) <br>
- [Self-Hosting Reference Guide](references/self_hosting.md) <br>
- [Firecrawl GitHub Repository](https://github.com/firecrawl/firecrawl) <br>
- [Firecrawl Advanced Scraping Guide](https://docs.firecrawl.dev/advanced-scraping-guide) <br>
- [Firecrawl Agent Endpoint](https://docs.firecrawl.dev/features/agent) <br>
- [Firecrawl Rate Limits](https://docs.firecrawl.dev/rate-limits) <br>
- [Firecrawl Self-Hosting Guide](https://raw.githubusercontent.com/firecrawl/firecrawl/main/SELF_HOST.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline code blocks, API request examples, configuration snippets, and JSON/schema examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a Firecrawl API key or a protected self-hosted Firecrawl endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
