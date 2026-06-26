## Description: <br>
Crawls Douyin trending video and caption data with Playwright, including keyword search, hot-list retrieval, video analysis, and natural-language request parsing. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to search Douyin content, inspect hot-list items, analyze individual Douyin video links, and turn scraped results into user-facing summaries or export files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Playwright browser automation can reach live Douyin pages and may trigger platform controls or account risk. <br>
Mitigation: Use the skill only for Douyin URLs, avoid logging into accounts, keep request rates low, and follow Douyin platform rules. <br>
Risk: The skill can write JSON or CSV export files. <br>
Mitigation: Review output paths before saving and run the skill in a workspace where generated files are expected. <br>
Risk: The analyze command accepts user-provided URLs. <br>
Mitigation: Restrict analyze inputs to Douyin URL patterns before execution. <br>
Risk: Installation may add local dependencies and browser binaries. <br>
Mitigation: Install in an isolated virtual environment or container and review dependency changes before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/terrycarter1985/douyin-scraper-pro) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Playwright documentation](https://playwright.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown summaries and command guidance, with scraper data available as JSON or CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include video titles, descriptions, authors, engagement counts, URLs, tags, and publish times.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
