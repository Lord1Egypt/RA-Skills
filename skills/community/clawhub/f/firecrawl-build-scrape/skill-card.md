## Description: <br>
Integrate Firecrawl `/scrape` into product code for single-page extraction when an app already has a URL and needs markdown, HTML, links, screenshots, metadata, or structured page output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eohmig](https://clawhub.ai/user/eohmig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add focused Firecrawl page scraping to products that already have a target URL. It supports page-level ingestion, enrichment, monitoring, and extraction workflows without broad crawling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Firecrawl requests can send target URLs and scraped page content to Firecrawl or a configured self-hosted endpoint. <br>
Mitigation: Use only approved pages and endpoints, avoid private or regulated content without approved data-handling terms, and keep the Firecrawl trust boundary explicit. <br>
Risk: The skill requires a Firecrawl API key for hosted requests. <br>
Mitigation: Store the API key in the declared FIRECRAWL_API_KEY environment variable and avoid exposing it in generated code, logs, or shared examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eohmig/firecrawl-build-scrape) <br>
- [Firecrawl homepage](https://www.firecrawl.dev) <br>
- [Firecrawl Node / TypeScript source of truth](https://docs.firecrawl.dev/agent-source-of-truth/node) <br>
- [Firecrawl Python source of truth](https://docs.firecrawl.dev/agent-source-of-truth/python) <br>
- [Firecrawl REST source of truth](https://docs.firecrawl.dev/agent-source-of-truth/curl) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown guidance with API integration recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Firecrawl `/scrape` request options, response format choices, and environment variable setup notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
