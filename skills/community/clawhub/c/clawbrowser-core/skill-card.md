## Description: <br>
Headless browser automation for AI agents with ARIA ref element targeting, natural-language actions, web scraping, and OpenClaw integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yesimagine-oss](https://clawhub.ai/user/yesimagine-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to drive browser sessions, inspect accessibility snapshots, interact with page elements, and extract page content for automation, testing, data collection, and RPA workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation and scraping can capture content from authenticated, private, or sensitive pages. <br>
Mitigation: Run in an isolated environment and avoid authenticated or private pages unless their contents are intended to be processed and stored. <br>
Risk: The scraper can export scraped page content to Feishu in CLI and scheduled modes without clear top-level disclosure. <br>
Mitigation: Do not use web_scraper CLI or scheduled mode unless Feishu export is intended; disable or edit the Feishu export path for local-only automation. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/yesimagine-oss/clawbrowser-core) <br>
- [agent-browser documentation](https://agent-browser.dev) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, shell commands, browser action results, accessibility snapshots, and extracted page content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, npm, agent-browser, and Chrome or Chromium; browser snapshots must be refreshed for dynamic content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
