## Description:

Web data for everyone. Powered by Firecrawl. Scrape, search, crawl, interact with websites - all in plain language. No technical skills needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search the web, scrape pages, map or crawl sites, interact with webpages, and extract structured data through Firecrawl using plain-language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested URLs, search terms, page content, and interaction or extraction instructions are sent to Firecrawl for processing.

Mitigation: Avoid sensitive, confidential, private, or regulated sites and data unless the user has approved that disclosure.

Risk: Interact commands can click, fill forms, log in, or download files on websites after confirmation.

Mitigation: Confirm the exact site and intended action before use, and operate only on sites the user owns or is authorized to control.

Risk: Crawling can batch-access many pages and may conflict with site terms or place load on the target site.

Mitigation: Respect robots.txt, site terms, and reasonable crawl limits before starting a crawl.

Risk: The skill may return Chinese-language output and Firecrawl branding by design.

Mitigation: Set user expectations for language and branding, or update the skill before deployment where that output is unsuitable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobewin/skills/firecrawl-wrapper)
- [Firecrawl documentation](https://docs.firecrawl.dev)
- [Firecrawl GitHub repository](https://github.com/firecrawl/firecrawl)
- [Firecrawl website](https://www.firecrawl.dev)
- [Firecrawl pricing](https://www.firecrawl.dev/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Firecrawl search results, scraped markdown, crawled page previews, extracted structured data, interaction results, error guidance, and Firecrawl branding.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
