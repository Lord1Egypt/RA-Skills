## Description: <br>
Firecrawl API integration with managed authentication for scraping, crawling, mapping, searching, extracting web content, and running browser or agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to call Firecrawl through Maton-managed authentication to scrape pages, crawl sites, map URLs, search the web, perform structured extraction, and manage browser or agent jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive credentials and may expose submitted URLs, prompts, page content, headers, connection URLs, or browser session URLs to Maton and Firecrawl. <br>
Mitigation: Install only when Maton and Firecrawl are trusted for the intended data, keep MATON_API_KEY and session URLs private, and avoid submitting sensitive content unless approved. <br>
Risk: Crawls, browser actions, custom headers, and agent jobs can interact with websites and consume credits. <br>
Mitigation: Require explicit approval for target URLs, crawl scope, limits, browser actions, custom headers, and agent jobs before execution. <br>
Risk: Large crawls or unconstrained agent jobs can use significant Firecrawl credits. <br>
Mitigation: Set reasonable crawl limits, maxDepth, and maxCredits values before starting large or autonomous jobs. <br>


## Reference(s): <br>
- [ClawHub Firecrawl Skill Page](https://clawhub.ai/byungkyu/firecrawl-api) <br>
- [Publisher Profile](https://clawhub.ai/user/byungkyu) <br>
- [Maton Homepage](https://maton.ai) <br>
- [Firecrawl API Documentation](https://docs.firecrawl.dev/api-reference/v2-introduction) <br>
- [Firecrawl Dashboard](https://firecrawl.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with Python and JavaScript code examples, shell commands, and JSON API payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY; operations can consume Firecrawl credits.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
