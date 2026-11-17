## Description:

AI-powered web scraping framework for extracting structured data from websites. Use when Codex needs to crawl, scrape, or extract data from web pages using AI-powered parsing, handle dynamic content, or work with complex HTML structures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codylrn804](https://clawhub.ai/user/codylrn804)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to guide agents through web scraping, crawling, and structured extraction from public or authorized web pages, including JavaScript-rendered content and complex HTML. It supports generating Python examples, shell commands, and output-file workflows for single-page, multi-page, and local HTML extraction tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs, including pages outside the user's intended scope.

Mitigation: Use only public or explicitly authorized URLs, and avoid authenticated, internal, or private-network pages.

Risk: Scraped page contents may be saved to disk and could include sensitive or unwanted data.

Mitigation: Review output paths before execution and inspect saved files before sharing, committing, or reusing them.

Risk: Batch scraping can create excessive requests or capture more content than intended.

Mitigation: Set conservative page counts and delays, and confirm the target site's robots.txt and terms before scraping.

## Reference(s):

- [Crawl4ai API Reference](references/api_reference.md)
- [Crawl4ai Examples](references/examples.md)
- [Crawl4ai Error Handling and Troubleshooting](references/error_handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; helper scripts can write JSON, Markdown, HTML, screenshots, and extracted web content files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save scraped page contents to user-selected files or directories.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
