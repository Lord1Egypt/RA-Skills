## Description:

为代理提供抖音关键词搜索和热榜查询命令，可输出视频标题、作者、互动计数、链接和标签字段；当前实现可能返回模拟示例数据。

This skill is for research and development only.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can ask an agent in Chinese to run Douyin keyword search or hot-list collection workflows and save video-style result records for analysis. Treat outputs as example data unless the publisher verifies real extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises Douyin scraping while current search and hot-list results may be synthetic example data.

Mitigation: Treat results as examples unless the publisher verifies extraction, and disclose uncertainty when using the data.

Risk: The skill may contact Douyin, install browser automation components, and create local output files.

Mitigation: Run it only in an isolated environment, review install scripts before execution, avoid logging into accounts, and comply with platform rules.

Risk: Browser setup includes risky automation choices that should be contained before installation.

Mitigation: Prefer a sandboxed container or other restricted runtime and review browser launch flags before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/douyin-scraper-terrycarter)
- [Playwright documentation](https://playwright.dev/)

## Skill Output:

**Output Type(s):** [text, shell commands, JSON, CSV files, guidance]

**Output Format:** [Console text and optional JSON or CSV output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records include title, description, author, play_count, like_count, comment_count, share_count, url, tags, and publish_time; browser fallback can produce synthetic examples.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
