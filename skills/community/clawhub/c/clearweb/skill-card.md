## Description: <br>
ClearWeb helps shell-capable AI agents search the web, read pages, extract structured data, and capture screenshots through the Bright Data CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meirk-brd](https://clawhub.ai/user/meirk-brd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use ClearWeb to perform web research, competitive analysis, lead generation, price monitoring, documentation reading, and structured extraction from supported public web platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad web-scraping and anti-bot access through a credentialed external service. <br>
Mitigation: Install only for authorized web access, prefer a dedicated low-privilege Bright Data account or API key with budget limits, and require explicit approval for bulk scraping or bot-defense bypass workflows. <br>
Risk: The skill can extract social-profile, lead-generation, paywall-adjacent, or other sensitive web data at scale. <br>
Mitigation: Apply site terms, privacy, and compliance review before use, and avoid private, internal, signed, or otherwise sensitive URLs. <br>
Risk: The setup path may install or authenticate a third-party CLI that controls external network access. <br>
Mitigation: Review the installer and account configuration before running it, store credentials securely, and monitor Bright Data usage and spend. <br>


## Reference(s): <br>
- [Web Search Reference](references/web-search.md) <br>
- [Web Scraping Reference](references/web-scrape.md) <br>
- [Structured Data Extraction Reference](references/data-extraction.md) <br>
- [Troubleshooting Reference](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI output formats including JSON, CSV, HTML, screenshots, and markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bright Data CLI authentication and may write requested scrape, screenshot, or extraction outputs to files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
