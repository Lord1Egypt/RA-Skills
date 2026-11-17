## Description:

Provides guidance and helper scripts for using a Dockerized Crawl4AI web crawling and scraping service through REST APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orange-afk](https://clawhub.ai/user/orange-afk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate a local Crawl4AI Docker service for web crawling, content extraction, screenshots, PDF generation, monitoring, and LLM-assisted extraction through REST API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sample deployment can expose a powerful crawler service more broadly than intended.

Mitigation: Bind the API to 127.0.0.1 unless remote access is explicitly needed, and place any remote deployment behind authentication and network filtering.

Risk: Using LLM-backed extraction can send private, regulated, or proprietary page content to external providers.

Mitigation: Avoid sending sensitive pages to external LLM providers without approval and use reviewed provider configuration.

Risk: The example container image uses a floating latest tag.

Mitigation: Pin the container image to a reviewed version or digest before production deployment.

## Reference(s):

- [Crawl4AI Documentation](https://docs.crawl4ai.com/)
- [ClawHub Skill Page](https://clawhub.ai/orange-afk/skills/crawl4ai-docker-skill)
- [Example Configuration](references/example-config.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Assumes a Crawl4AI Docker service is available, typically on localhost port 11235.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
