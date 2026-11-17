## Description:

Playwright-based web scraping OpenClaw Skill with anti-bot protection. Successfully tested on complex sites like Discuss.com.hk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to collect content from dynamic or anti-bot-protected web pages with Playwright-based simple and stealth scraping modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The stealth scraper can access arbitrary URLs and is designed for anti-bot-protected pages.

Mitigation: Use it only against sites the operator is authorized to access, and run it in a disposable, low-privilege environment with restricted network access.

Risk: The scraper can write screenshots and optional HTML captures to local paths.

Mitigation: Choose non-sensitive output locations and avoid scraping authenticated or sensitive pages unless necessary.

Risk: The stealth mode weakens browser safety controls.

Mitigation: Review the scripts before deployment and keep execution isolated from credentials and sensitive local files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smallkeyboy/skills/102-playwright-scraper-skill)
- [Playwright official docs](https://playwright.dev/)
- [puppeteer-extra-plugin-stealth](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth)
- [deep-scraper skill](https://clawhub.com/opsun/deep-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands; scraper scripts emit JSON and may write screenshot or HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output may include page title, URL, content previews, elapsed time, Cloudflare detection status, extracted links, screenshot paths, and optional HTML capture paths.]

## Skill Version(s):

1.2.0 (source: frontmatter, package.json, CHANGELOG released 2026-02-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
