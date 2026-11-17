## Description:

爬取抖音热榜和搜索建议数据，支持关键词搜索、热榜获取、搜索建议等功能。无需登录即可使用。

This skill is for research and development only.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to fetch Douyin hot-search topics, match keywords against the hot list, and retrieve search suggestions for trend monitoring or content research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can download mutable Python, Playwright, browser, mirror-hosted, and Docker assets that are broader than the API-only scraper normally needs.

Mitigation: Prefer the API-only Node.js or Python scripts when possible, pin and review dependencies before installation, and run browser or Docker setup only in an isolated environment.

Risk: Frequent Douyin API requests can fail or trigger IP controls.

Mitigation: Throttle usage, follow the artifact guidance to keep requests at least five seconds apart, and stop or retry later if responses indicate rate limiting.

Risk: Full Douyin search may require a logged-in browser session or cookie outside the default no-login workflow.

Mitigation: Use the hot-list and suggestion modes by default; provide login cookies only when necessary and handle them as sensitive credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/douyin-scraper-v2)
- [Douyin web service](https://www.douyin.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save hot-search, search, and suggestion results as JSON when an output file is provided.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
