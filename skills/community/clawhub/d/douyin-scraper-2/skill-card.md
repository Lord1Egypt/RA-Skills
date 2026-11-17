## Description:

爬取抖音爆款视频和文案数据，支持自然语言搜索请求（如"搜索一下海鲜视频"），通过浏览器自动化或脚本获取数据。

This skill is for research and development only.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to search Douyin videos, inspect hot-list content, or extract video metadata from natural-language requests. The artifact states the data is for learning and research use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Logged-in browser automation may expose a user's primary Douyin session to scraping workflows.

Mitigation: Use an isolated browser profile or test account rather than a primary logged-in session.

Risk: Real scraping paths can return mock sample records when browser automation is unavailable or blocked.

Mitigation: Label results as sample data unless live extraction is verified for the current run.

Risk: The browser scripts can launch Chromium with reduced sandboxing.

Mitigation: Run the skill in a disposable environment and avoid unsandboxed browser execution on sensitive machines.

Risk: Installation fetches Playwright and browser dependencies.

Mitigation: Pin or verify dependencies before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/douyin-scraper-2)
- [Douyin search](https://www.douyin.com/search/{keyword}?type=video)
- [Douyin hot list](https://www.douyin.com/hot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, console text, JSON, or CSV depending on the selected workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Script output may fall back to mock sample records when browser automation is unavailable or blocked.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
