## Description: <br>
Web search and scraping via the Firecrawl API for search, single-page scraping, site crawling, and structured web extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ashwingupy](https://clawhub.ai/user/ashwingupy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to search the web, scrape pages, crawl websites, and collect Firecrawl results for downstream analysis or content extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, URLs, and retrieved page content are sent to Firecrawl under the configured API key. <br>
Mitigation: Avoid internal, private, token-bearing, or regulated URLs unless that data sharing is approved. <br>
Risk: Crawl commands can consume Firecrawl quota or create billing exposure. <br>
Mitigation: Set conservative crawl limits and monitor Firecrawl usage and billing. <br>


## Reference(s): <br>
- [Firecrawl API Reference](references/api.md) <br>
- [Firecrawl pricing](https://firecrawl.dev/pricing) <br>
- [ClawHub release page](https://clawhub.ai/ashwingupy/firecrawl-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON responses from Firecrawl-backed command-line workflows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FIRECRAWL_API_KEY and sends search terms, target URLs, and retrieved page content to Firecrawl.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
