## Description: <br>
AI-powered web scraping framework for extracting structured data from websites. Use when Codex needs to crawl, scrape, or extract data from web pages using AI-powered parsing, handle dynamic content, or work with complex HTML structures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codylrn804](https://clawhub.ai/user/codylrn804) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to scrape, crawl, clean, and extract structured data from web pages, including JavaScript-driven pages and complex HTML. It supports authorized extraction workflows for products, articles, tables, forms, links, markdown, clean HTML, screenshots, and batch scraping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports browser-based scraping and includes guidance that could be applied to sites where scraping is not authorized. <br>
Mitigation: Use it only on sites and pages the user is authorized to access, and check robots.txt and terms of service before scraping. <br>
Risk: The security review notes anti-bot bypass advice and Cloudflare or proxy guidance. <br>
Mitigation: Avoid bypass-oriented guidance and do not use proxies or anti-bot workarounds unless there is explicit authorization and a legitimate operational need. <br>
Risk: The artifact includes an unrelated GitHub CLI login instruction. <br>
Mitigation: Do not run gh auth login for this skill unless a separate GitHub task specifically requires it. <br>
Risk: Scraped HTML, screenshots, and extracted records can contain personal, confidential, or otherwise sensitive information. <br>
Mitigation: Store outputs only where appropriate, minimize collected data, and review outputs before sharing or committing them. <br>


## Reference(s): <br>
- [Crawl4ai ClawHub release](https://clawhub.ai/codylrn804/crawl4ai) <br>
- [Crawl4ai API Reference](references/api_reference.md) <br>
- [Crawl4ai Examples](references/examples.md) <br>
- [Crawl4ai Error Handling and Troubleshooting](references/error_handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code blocks; helper scripts can emit markdown, HTML, JSON, screenshots, and saved files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include scraped page content and screenshots; treat saved HTML, screenshots, and extracted records as potentially sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
