## Description: <br>
Browser Automation helps agents scrape, crawl, screenshot, and interact with JavaScript-rendered websites using Puppeteer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fasjdas](https://clawhub.ai/user/fasjdas) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation agents use this skill to extract structured content, crawl paginated pages, capture screenshots, and build browser workflows for websites that require JavaScript rendering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can access sites, submit forms, and interact with pages in ways that may violate site terms, robots.txt, or rate limits. <br>
Mitigation: Review site terms, robots.txt, and rate limits before running the skill, and add delays or page limits for crawls. <br>
Risk: Running the skill on logged-in, payment, crypto, or sensitive account pages could expose private data or trigger unintended actions. <br>
Mitigation: Use it on authenticated, payment, crypto, or sensitive pages only when the user explicitly intends that automation and has confirmed the target account and action. <br>


## Reference(s): <br>
- [Browser Automation README](README.md) <br>
- [Puppeteer API Reference](references/puppeteer-api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/fasjdas/browser-automation-puppeteer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, files, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell snippets; helper scripts emit JSON data or PNG screenshot files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, npm, Puppeteer, and network access to user-selected websites.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
