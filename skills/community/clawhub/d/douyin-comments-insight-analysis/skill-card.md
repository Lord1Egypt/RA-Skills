## Description:

抓取抖音关键词搜索结果、作品详情、博主作品、评论和热榜，并输出结构化数据供内容与舆情分析使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content, product, and customer support teams can search public Douyin videos, review creator posts and comments, and track trending topics. Agents can use the returned structured data for content planning, competitor research, and audience feedback analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Douyin links are sent to the third-party API at www.guaikei.com.

Mitigation: Only submit queries and links that are appropriate to share with that provider.

Risk: The API token is required for requests, and provider usage may incur charges.

Mitigation: Keep GUAIKEI_API_TOKEN private and check provider charges before making requests.

Risk: Locally saved logs can include public usernames, comments, and location labels; the provider's retention practices were not verified.

Mitigation: Limit access to saved logs, delete them when no longer needed, and review provider terms before sending sensitive queries.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/douyin-comments-insight-analysis)
- [Guaikei API provider](https://www.guaikei.com)
- [Command options](references/options.md)
- [Comment demand-mining guide](references/demand-mining.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON on command-line stdout, with results also saved locally]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A response envelope contains status, request details, and structured Douyin results; agents can summarize the data for research and monitoring.]

## Skill Version(s):

1.4.2 (source: frontmatter, package.json, changelog released 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
