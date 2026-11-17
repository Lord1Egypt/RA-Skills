## Description:

Scrapling helps agents install and use the Scrapling Python web scraping framework for adaptive extraction, browser automation, spider workflows, and MCP-assisted data collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to guide agents through Scrapling installation, fetcher selection, scraping code generation, browser-driver setup, spider configuration, proxy usage, and troubleshooting for web data extraction tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents toward anti-bot bypass, browser automation, proxy use, and high-volume scraping that may conflict with site terms, authorization, privacy, or rate limits.

Mitigation: Use only for authorized targets; check site terms, robots and rate-limit requirements; reduce concurrency where needed; and keep scraped sensitive or access-restricted data out of AI and MCP workflows.

Risk: Persistent MCP registration or agent-run shell commands can broaden access beyond the immediate scraping task.

Mitigation: Prefer project-scoped MCP registration, pin package and Docker versions, and review installation, browser-driver, proxy, and MCP commands before execution.

## Reference(s):

- [Scrapling documentation](https://scrapling.readthedocs.io)
- [Scrapling latest documentation](https://scrapling.readthedocs.io/en/latest/)
- [Scrapling PyPI package](https://pypi.org/project/scrapling/)
- [Scrapling MCP server documentation](https://scrapling.readthedocs.io/en/latest/ai/mcp-server.html)
- [Scrapling GitHub project](https://github.com/D4Vinci/Scrapling)
- [Scrapling Spider architecture](https://scrapling.readthedocs.io/en/latest/spiders/architecture.html)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python, shell, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend browser automation, MCP registration, proxy configuration, and local file or database state for adaptive scraping workflows.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
