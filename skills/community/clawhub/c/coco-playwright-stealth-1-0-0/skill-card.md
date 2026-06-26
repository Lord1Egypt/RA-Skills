## Description: <br>
Playwright-based web scraping OpenClaw Skill with anti-bot protection, tested on complex sites like Discuss.com.hk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gu-yunyu](https://clawhub.ai/user/gu-yunyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to fetch content from JavaScript-heavy or anti-bot-protected websites with Playwright scripts. It can return scraped page metadata and content previews, and can optionally save screenshots or HTML captures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan says the skill promotes anti-bot bypassing and may violate site rules or laws when used without permission. <br>
Mitigation: Use it only for sites where you have permission, review the target site's terms, and avoid stealth or proxy behavior unless it is authorized. <br>
Risk: The skill can weaken browser containment and run a downloaded Chromium browser against arbitrary URLs. <br>
Mitigation: Install dependencies deterministically, run the skill in an isolated environment, and avoid logged-in, sensitive, or internal-only pages. <br>
Risk: Screenshots and saved HTML can capture sensitive page content. <br>
Mitigation: Review generated screenshots and HTML before sharing, and disable capture options when they are not needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gu-yunyu/coco-playwright-stealth-1-0-0) <br>
- [Playwright Official Docs](https://playwright.dev/) <br>
- [puppeteer-extra-plugin-stealth](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth) <br>
- [deep-scraper skill](https://clawhub.com/opsun/deep-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-like scraper output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts may save screenshot PNG files and optional HTML captures when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter, package.json, and changelog report 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
