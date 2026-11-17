## Description:

爬取抖音爆款视频和文案数据，使用 Playwright 自动化浏览器操作，支持搜索关键词、获取热榜、提取视频信息和文案等功能。

This skill is for research and development only.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to search Douyin keywords, inspect hot-list categories, and summarize video metadata and copywriting signals for review. Use it only where platform rules, account privacy, and scraping permissions are understood.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs browser automation with network access and can write local result files.

Mitigation: Install and run it only in an environment where outbound access and writable paths are acceptable.

Risk: Cookie files or logged-in browser sessions can expose account and privacy data.

Mitigation: Avoid passing cookies or using a logged-in session unless the operator has explicit authorization and understands the account risk.

Risk: Natural-language requests may be transformed into shell commands.

Mitigation: Invoke the scraper with structured arguments and validate or quote user-supplied keywords before execution.

Risk: CAPTCHA, browser setup failures, or Douyin page changes may produce mock, stale, or incomplete output.

Mitigation: Verify whether results came from live extraction before using them for decisions.

Risk: Frequent scraping can conflict with platform rules or trigger IP and anti-abuse controls.

Mitigation: Respect Douyin rules and applicable law, use request delays, and stop if rate limits or blocking appear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/douyin-scraper-v3)
- [ClawHub publisher profile](https://clawhub.ai/user/terrycarter1985)
- [Playwright documentation](https://playwright.dev/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown summaries with shell commands and optional JSON or CSV output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return mock or incomplete data when live extraction is blocked by CAPTCHA, browser setup, or page changes.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
