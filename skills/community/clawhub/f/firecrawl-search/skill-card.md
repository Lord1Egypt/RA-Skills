## Description:

Firecrawl Search provides web search and scraping via the Firecrawl API for searching the web, scraping pages, crawling sites, and extracting structured page data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashwingupy](https://clawhub.ai/user/ashwingupy)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to search the web, scrape individual pages, crawl websites, and retrieve structured page content through Firecrawl.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends search queries and target URLs to Firecrawl as an external web search and scraping service.

Mitigation: Use it only for data your organization approves sharing with Firecrawl; avoid secret-bearing URLs, internal-only links, authenticated pages, customer data, and regulated content unless approved.

Risk: The Firecrawl API key is required for operation and could be exposed if handled carelessly.

Mitigation: Keep FIRECRAWL_API_KEY out of source control and rotate it if exposed.

## Reference(s):

- [Firecrawl API Reference](references/api.md)
- [Firecrawl pricing](https://firecrawl.dev/pricing)
- [ClawHub skill page](https://clawhub.ai/ashwingupy/skills/firecrawl-search)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or JSON returned from Firecrawl helper commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FIRECRAWL_API_KEY and sends submitted search queries or URLs to Firecrawl.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
