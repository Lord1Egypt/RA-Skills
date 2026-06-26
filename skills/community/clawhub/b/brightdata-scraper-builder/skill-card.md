## Description: <br>
Build production-ready web scrapers for websites using Bright Data infrastructure, including site analysis, API selection, selector extraction, pagination handling, and complete scraper implementation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meirk-brd](https://clawhub.ai/user/meirk-brd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to create and validate Bright Data-based scrapers for extracting structured data from websites, including static pages, JavaScript-rendered pages, paginated listings, and sites with pre-built Bright Data scrapers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the generated scraper can send target URLs and fetched content to Bright Data. <br>
Mitigation: Use the skill only for Bright Data scraping workflows, avoid private or secret-bearing URLs unless approved, and review the generated scraper before running it. <br>
Risk: Bright Data API credentials are required for generated examples and may be exposed if hardcoded or logged. <br>
Mitigation: Use scoped API credentials through environment variables and avoid committing, printing, or sharing credential values. <br>
Risk: Generated scrapers may create more requests than intended when page or concurrency limits are too broad. <br>
Mitigation: Validate on a small sample first, set explicit page and concurrency limits, and scale only after the extracted data is correct. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/meirk-brd/brightdata-scraper-builder) <br>
- [Supported domains](references/supported-domains.md) <br>
- [Site analysis guide](references/site-analysis-guide.md) <br>
- [Pagination patterns](references/pagination-patterns.md) <br>
- [Concurrency guide](references/concurrency-guide.md) <br>
- [Bright Data documentation index](https://docs.brightdata.com/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with runnable scraper code, shell commands, configuration notes, and JSON-oriented output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated scrapers commonly use Bright Data credentials, target URLs, page limits, concurrency limits, and sample validation runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
