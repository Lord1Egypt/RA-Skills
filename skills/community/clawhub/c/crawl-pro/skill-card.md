## Description:

Crawl Pro is a Scrapling-based workflow for production web scraping with adaptive element location, anti-bot handling, concurrent crawling, checkpointing, proxy rotation, and data export guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smseow001](https://clawhub.ai/user/smseow001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and generate web scraping workflows that select appropriate Scrapling fetchers, parse content, run concurrent crawls, resume interrupted jobs, rotate proxies, and export collected data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill teaches anti-bot bypass, proxy rotation, and scaled collection without built-in authorization or compliance guardrails.

Mitigation: Use it only for sites you own or are authorized to crawl, and add checks for robots.txt, site terms, rate limits, privacy, and data retention before deployment.

Risk: The workflow depends on Scrapling installation and browser-backed fetching paths that may change runtime behavior or expand permissions.

Mitigation: Pin and review the Scrapling dependency in an isolated environment, avoid privileged installs, and scan generated scraper code before execution.

## Reference(s):

- [Crawl Pro on ClawHub](https://clawhub.ai/smseow001/skills/crawl-pro)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scraper templates, fetcher selection guidance, concurrency settings, export formats, and MCP integration steps.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
