## Description:

Web scraping, crawling, searching, and browser automation via the Firecrawl CLI for scraping URLs, crawling websites, discovering site URLs, running web searches with optional scraping, launching cloud browser sessions, and using natural-language web queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yash-kavaiya](https://clawhub.ai/user/yash-kavaiya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate the Firecrawl CLI for web scraping, site crawling, URL discovery, search workflows, cloud browser automation, and natural-language web research tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Firecrawl uses authentication credentials and can access web content through a third-party cloud scraping or browser automation service.

Mitigation: Use browser login or a secret manager for credentials, avoid pasting API keys into commands, and only scrape sensitive, internal, or authenticated pages when approved.

Risk: Global installation of the Firecrawl CLI through npm can execute third-party package code on the agent environment.

Mitigation: Review or pin the npm package before global installation when operating in controlled or production environments.

Risk: Reusable cloud browser sessions or profiles can retain private browsing state.

Mitigation: Close cloud browser sessions after use and avoid reusable profiles when retained state could expose private data.

## Reference(s):

- [Firecrawl CLI Command Reference](references/commands.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown, Code]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or direct users to Firecrawl CLI outputs such as markdown, HTML, JSON, links, images, screenshots, summaries, saved files, and browser session command results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
