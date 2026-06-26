## Description: <br>
AnyCrawl-API lets agents scrape pages, run Google search, and crawl websites through the AnyCrawl API with multiple extraction engines and structured output formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[techlaai](https://clawhub.ai/user/techlaai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to collect web content, search results, and crawl output for research, data extraction, monitoring, and retrieval workflows through an AnyCrawl API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys could be exposed or overprivileged if shared broadly or stored insecurely. <br>
Mitigation: Use a revocable AnyCrawl API key, store it in environment or approved gateway configuration, and rotate it if exposure is suspected. <br>
Risk: Scraping or crawling private, internal, or sensitive URLs can expose data to a third-party service. <br>
Mitigation: Only submit URLs and content approved for processing by AnyCrawl, and avoid private or internal targets unless explicitly authorized. <br>
Risk: Broad crawls can consume quota, expand collection scope, or hit rate limits. <br>
Mitigation: Set conservative crawl depth, page limits, include/exclude paths, and safe search or language settings appropriate to the task. <br>


## Reference(s): <br>
- [ClawHub AnyCrawl-API Release Page](https://clawhub.ai/techlaai/anycrawl) <br>
- [AnyCrawl API Documentation](https://docs.anycrawl.dev) <br>
- [AnyCrawl API Key Setup](https://anycrawl.dev) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Text, Configuration guidance, Shell commands] <br>
**Output Format:** [Structured JSON API responses that may include scraped markdown, HTML, text, JSON extraction results, screenshots, crawl job metadata, and setup commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ANYCRAWL_API_KEY and depends on AnyCrawl service limits, credits, rate limits, and crawl job expiration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
