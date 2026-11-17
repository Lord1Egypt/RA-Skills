## Description:

抖音热门视频搜索工具，支持按关键词搜索获取最多点赞热门内容数据，基于抖音的实时数据返回特定关键词的热门视频数据，助力创作者、品牌方和MCN机构发现热门趋势、获取创作灵感。支持五大能力：(1) 关键词搜索视频/图文，可按点赞数、发布时间、视频时长、内容类型筛选排序；(2) 实时热榜查询，获取抖音热搜词条与热度数据；(3) 单条作品详情，按视频链接或 aweme_id 获取文案、互动与作者；(4) 博主作品抓取，按主页链接或 sec_uid 获取公开作品列表；(5) 视频评论分析，按视频链接或 aweme_id 获取评论内容与互动数据；评论需求/痛点挖掘（取评后见 demand-mining）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

内容创作者、品牌团队和数据分析人员可用它检索抖音公开视频、图文、博主作品、评论与热榜数据，为选题、竞品观察和舆情分析提供结构化资料。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is marked benign, but static analysis was partial and its confidence is medium.

Mitigation: Review the declared scope and environment-variable access before use, and install only if comfortable with the remaining uncertainty.

Risk: Queries send the supplied keyword or Douyin link to the third-party Guaikei API, and access depends on GUAIKEI_API_TOKEN.

Mitigation: Use only queries you are comfortable sharing with that provider, and keep the API token confidential.

Risk: The skill retrieves public user-generated content and its documentation limits use to personal or team analysis and prohibits unauthorized distribution.

Mitigation: Use returned content for internal analysis and follow applicable platform and data-use requirements before sharing it.

## Reference(s):

- [抖音数据 API 服务](https://www.guaikei.com)
- [ClawHub skill release](https://clawhub.ai/why20261/skills/douyin-videos-search)
- [Command options](references/options.md)
- [Demand mining guide](references/demand-mining.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON response envelopes and concise analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include public post, author, engagement and comment data; media links may expire. Query volume depends on the API plan.]

## Skill Version(s):

1.4.2 (source: frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
