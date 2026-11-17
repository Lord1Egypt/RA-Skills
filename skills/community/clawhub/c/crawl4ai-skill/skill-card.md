## Description:

Web crawling and scraping tool with LLM-optimized output, DuckDuckGo search, site crawling, and dynamic page scraping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lancelin111](https://clawhub.ai/user/lancelin111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search the web, scrape individual pages, crawl documentation or websites, and produce LLM-optimized Markdown from static or JavaScript-rendered pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs network crawling and scraping, which can create legal, privacy, copyright, site-policy, or rate-limit issues if used carelessly.

Mitigation: Respect site terms, robots.txt, privacy boundaries, copyright, and conservative rate and page limits.

Risk: Running a third-party scraping wrapper in a shared environment may expose the user to unreviewed package behavior.

Mitigation: Install and run it in a virtual environment or container, avoid elevated privileges, and pin a reviewed package version before production use.

## Reference(s):

- [Crawl4ai Skill on ClawHub](https://clawhub.ai/lancelin111/skills/crawl4ai-skill)
- [Crawl4ai Skill GitHub Repository](https://github.com/lancelin111/crawl4ai-skill)
- [crawl4ai-skill on PyPI](https://pypi.org/project/crawl4ai-skill/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and command output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports fit_markdown and raw_markdown output modes, optional output files, page limits, crawl depth, wait strategies, delays, and selectors.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
