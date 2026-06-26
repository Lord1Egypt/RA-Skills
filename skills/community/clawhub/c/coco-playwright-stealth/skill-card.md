## Description: <br>
Playwright-based web scraping OpenClaw Skill with anti-bot protection. Successfully tested on complex sites like Discuss.com.hk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to scrape dynamic or anti-bot-protected websites with Playwright, choosing a simple browser run for normal pages or a stealth-oriented run for sites that block obvious automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed for scraping and includes anti-bot behavior, which can be inappropriate on sites where the user lacks authorization. <br>
Mitigation: Use it only for sites and content the operator is authorized to access and scrape, and review target-site terms before running. <br>
Risk: Screenshots and saved HTML can capture sensitive page content on local disk. <br>
Mitigation: Avoid authenticated or private pages unless outputs can be protected, reviewed, and deleted after use. <br>
Risk: Playwright downloads and runs browser binaries in the execution environment. <br>
Mitigation: Prefer a disposable, containerized, or otherwise isolated workspace when installing and running the skill. <br>


## Reference(s): <br>
- [Playwright Official Docs](https://playwright.dev/) <br>
- [puppeteer-extra-plugin-stealth](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth) <br>
- [deep-scraper skill](https://clawhub.com/opsun/deep-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands; scraper scripts emit JSON plus optional screenshot and HTML files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses environment variables for wait time, headless mode, screenshot path, HTML saving, and custom user agent.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter, package.json, changelog, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
