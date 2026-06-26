## Description: <br>
ClawBrowser provides browser automation and web scraping utilities for agents using agent-browser, ARIA references, natural-language commands, snapshots, and content extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yesimagine-oss](https://clawhub.ai/user/yesimagine-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to open pages, inspect accessibility snapshots, interact with elements, extract page text, images, and links, and save scraped results for downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation and scraping may capture sensitive content from logged-in, internal, or confidential pages. <br>
Mitigation: Use isolated browser sessions, avoid entering secrets through this wrapper, and review the skill before using it on sensitive pages. <br>
Risk: The scraper can upload captured page content to Feishu by default in CLI scrape, batch, and scheduled modes. <br>
Mitigation: Change or wrap web_scraper.py so Feishu upload requires an explicit per-run choice, and confirm the destination before running CLI modes. <br>
Risk: Extracted web content and browser actions depend on live third-party pages and may be incomplete, stale, or misleading. <br>
Mitigation: Review extracted content and planned actions before using them in downstream decisions or workflows. <br>


## Reference(s): <br>
- [ClawBrowser Skill on ClawHub](https://clawhub.ai/yesimagine-oss/clawbrowser-skill) <br>
- [agent-browser documentation](https://agent-browser.dev) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Python API results, CLI output, JSON scrape records, Markdown scrape exports, and setup commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, npm, agent-browser, and Chrome or Chromium. The scraper can save page content locally and CLI modes can upload captured content to Feishu.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
