## Description:

爬取抖音爆款视频和文案数据，使用 Playwright 自动化浏览器操作，支持搜索关键词、获取热榜、提取视频信息和文案等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to search Douyin keywords, retrieve trending-video data, and export parsed video metadata for downstream review or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser scraping and file-writing commands may run against live Douyin pages with limited user confirmation.

Mitigation: Require confirmation before scraping or writing output files, and run the skill only for approved keywords and destinations.

Risk: Installation and runtime behavior download browser automation components and launch Chromium.

Mitigation: Use an isolated, unprivileged environment with no sensitive files mounted and pin reviewed dependency versions.

Risk: The release uses unsafe browser and installation defaults according to the security summary.

Mitigation: Avoid running as root and review the installation and browser launch settings before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/douyin-search-scraper)
- [Playwright documentation](https://playwright.dev/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Terminal text with optional JSON or CSV output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on live Douyin pages, browser automation behavior, rate limits, and requested keyword, limit, category, and output format.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
