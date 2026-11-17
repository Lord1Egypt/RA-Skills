## Description:

AgentCrawl helps agents read web pages and documentation locally as clean Markdown, with options for JavaScript-rendered pages, targeted sections, site crawling, and structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jorg18](https://clawhub.ai/user/jorg18)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users can retrieve readable page content, inspect documentation sites, and extract selected page data without a hosted scraping service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the local scraper or optional browser automation adds software dependencies.

Mitigation: Review the installation before adding the CLI, MCP server, or optional browser components.

Risk: Broad crawls or private-network access may reach more pages than intended.

Mitigation: Set bounded crawl limits and enable private-network access only for local sites you intend to inspect.

Risk: A configured search integration uses an API key.

Mitigation: Keep the key scoped to the search service and do not expose it in page content or outputs.

## Reference(s):

- [AgentCrawl project homepage (skill metadata)](https://github.com/JorG18/agentcrawl)
- [AgentCrawl ClawHub release](https://clawhub.ai/jorg18/skills/agentcrawl)

## Skill Output:

**Output Type(s):** [Text, Markdown, Structured data, Guidance]

**Output Format:** [Markdown or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include page links, metadata, selected sections, and bounded multi-page results.]

## Skill Version(s):

0.6.0 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
