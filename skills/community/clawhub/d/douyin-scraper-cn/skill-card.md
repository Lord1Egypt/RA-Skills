## Description:

爬取抖音爆款视频和文案数据。支持自然语言搜索和结构化 CLI 调用，使用 Playwright 自动化浏览器，无浏览器时自动降级为模拟数据。

This skill is for research and development only.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to issue Chinese natural-language or structured CLI requests for Douyin video search, hot-list lookup, caption extraction, and JSON or CSV export. The artifact explicitly frames use as learning and research only.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may present simulated records as scraped Douyin results.

Mitigation: Treat returned records as mock data unless independently verified against live Douyin pages, and disclose verification status before downstream use.

Risk: Installation pulls Playwright and Chromium browser dependencies that are not fully pinned by the artifact.

Mitigation: Install in an isolated, non-privileged environment and pin, mirror, or verify Playwright and browser artifacts before use.

Risk: User-selected output paths can overwrite local files.

Mitigation: Write outputs only to scratch or project-specific paths and avoid paths containing important existing files.

Risk: Automated access to Douyin may conflict with platform rules or trigger account and IP restrictions.

Mitigation: Use conservative request rates, avoid logging in with personal accounts, and confirm compliance with applicable platform terms and laws before collection.

## Reference(s):

- [Playwright documentation](https://playwright.dev/)
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/douyin-scraper-cn)

## Skill Output:

**Output Type(s):** [text, JSON data, CSV data, shell commands]

**Output Format:** [Terminal text with optional JSON or CSV output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Falls back to simulated video records when Playwright or browser automation is unavailable.]

## Skill Version(s):

2.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
