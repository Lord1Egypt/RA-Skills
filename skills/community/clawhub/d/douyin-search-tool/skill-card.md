## Description:

抖音作品查询工具可通过 Node.js 命令查询抖音公开内容，支持关键词搜索、实时热榜、博主作品抓取和视频评论数据获取，并返回结构化 JSON 供后续分析使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and content or marketing analysts use this skill to retrieve public Douyin search results, trending topics, creator posts, and comments for content research, competitor monitoring, social listening, and reporting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, Douyin links, IDs, and the GUAIKEI_API_TOKEN are sent to the third-party guaikei.com API.

Mitigation: Install and run only when this data sharing is acceptable, keep the token in local environment variables, and avoid exposing terminal sessions or configuration that include credentials.

Risk: Saved JSON logs may contain sensitive business context or personal data from public Douyin profiles and comments.

Mitigation: Protect, minimize, and delete local logs when they are no longer needed, and de-identify user-facing reports before sharing outside the authorized team.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/why20261/skills/douyin-search-tool)
- [Server-Resolved GitHub Provenance](https://github.com/why20261/douyin-search-tool)
- [抖音达人数据获取官网](https://www.guaikei.com)
- [Complete Options](references/options.md)
- [Changelog](references/changelog.md)
- [Search CLI Request Schema](assets/search_cli_req.schema.json)
- [Search CLI Response Schema](assets/search_cli_resp.schema.json)
- [Post CLI Request Schema](assets/post_cli_req.schema.json)
- [Post CLI Response Schema](assets/post_cli_resp.schema.json)
- [Hot CLI Response Schema](assets/hot_cli_resp.schema.json)
- [Comment CLI Request Schema](assets/comment_cli_req.schema.json)
- [Comment CLI Response Schema](assets/comment_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Files, JSON, Guidance]

**Output Format:** [JSON results with stderr logs and optional saved JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; supports search, hot-list, creator-post, and comment commands.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
