## Description: <br>
Scrapling is a high-performance adaptive Python web scraping framework for AI-assisted data extraction, anti-bot workflows, adaptive element relocation, spider crawling, and MCP-based browser control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to install and apply Scrapling for authorized web data extraction, including choosing fetchers, writing CSS or XPath extraction code, configuring adaptive scraping, building spiders, and setting up MCP or CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide AI-assisted scraping and anti-bot bypass against sites where the user may not have authorization. <br>
Mitigation: Use it only for sites the user owns or is clearly authorized to access, and avoid anti-bot bypass or robots.txt overrides without explicit permission. <br>
Risk: Generated pip, Docker, browser-driver, MCP, proxy, and scraping commands can execute networked tooling or route traffic through third-party services. <br>
Mitigation: Review every command before execution, prefer isolated environments, and confirm that dependencies, proxy endpoints, and MCP servers are trusted. <br>
Risk: Adaptive snapshots, caches, sessions, and MCP workflows can retain or expose private, authenticated, regulated, or proprietary page data. <br>
Mitigation: Do not use these features on sensitive pages without a retention, access-control, and cleanup plan. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/cn-big-cabbage/cn-scrapling) <br>
- [Scrapling documentation](https://scrapling.readthedocs.io) <br>
- [Scrapling PyPI project](https://pypi.org/project/scrapling/) <br>
- [Scrapling MCP Server documentation](https://scrapling.readthedocs.io/en/latest/ai/mcp-server.html) <br>
- [Installation guide](artifact/guides/01-installation.md) <br>
- [Quickstart guide](artifact/guides/02-quickstart.md) <br>
- [Advanced usage guide](artifact/guides/03-advanced-usage.md) <br>
- [Troubleshooting guide](artifact/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python, shell, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include package installation commands, browser-driver setup, fetcher selection, scraping code, proxy/session configuration, MCP setup, and troubleshooting steps.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
