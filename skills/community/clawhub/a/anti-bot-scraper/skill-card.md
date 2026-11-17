## Description:

A Playwright-based web scraping skill that supports simple, stealth, and batch scraping modes, with optional CSS selector extraction, screenshots, HTML capture, cookies, proxies, and anti-detection browser behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tttyix](https://clawhub.ai/user/tttyix)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to collect web page text, links, images, metadata, screenshots, or saved HTML from authorized websites. It is suited to single-page collection, CSS-targeted extraction, and batch scraping workflows that need Playwright browser rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate browser scraping with stealth behavior and may be misused against websites where scraping is not authorized.

Mitigation: Use it only on websites where the operator has authorization, and review target site terms, robots.txt, and applicable policies before execution.

Risk: Cookie, proxy, browser, and install-time permissions can expose account context or route traffic through untrusted infrastructure.

Mitigation: Avoid account session cookies unless account-level actions are intended, use only trusted proxies, avoid localhost, private-network, and cloud metadata targets, and install in a sandbox with reviewed dependencies.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tttyix/skills/anti-bot-scraper)
- [Publisher Profile](https://clawhub.ai/user/tttyix)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and shell commands; scraper scripts emit JSON results and may write screenshot or HTML files when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [JSON scraper output includes success status, URL, title, content, links, images, metadata, and elapsed time.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
