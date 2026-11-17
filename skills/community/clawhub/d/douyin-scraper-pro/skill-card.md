## Description:

爬取抖音爆款视频和文案数据，支持自然语言搜索请求，并使用 Playwright 获取搜索、热榜和视频详情信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations users can ask an agent to search Douyin topics, inspect trending videos, or analyze a Douyin video URL, then receive summarized video metadata and copywriting signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scraper runs browser automation with local shell access and Chromium sandboxing disabled.

Mitigation: Run it in a restricted container or disposable environment with only the files and network access needed for the task.

Risk: The analyze command can browse user-supplied URLs.

Mitigation: Only analyze trusted Douyin URLs, avoid logged-in browser sessions, and do not provide secrets or private account context to the scraper.

Risk: Installation pulls mutable external dependencies and browser binaries.

Mitigation: Pin and verify dependencies before use, and prefer a reviewed container image or locked environment for repeatable execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/douyin-scraper-pro)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)
- [Playwright documentation](https://playwright.dev/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Agent-facing guidance plus JSON or CSV video metadata from scraper commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include title, description, author, engagement counts, URL, tags, and publish time; commands can write JSON or CSV files when an output path is provided.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
