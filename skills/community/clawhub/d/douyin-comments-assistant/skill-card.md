## Description:

用于抖音公开内容分析，支持关键词搜索、热榜查询、作品详情、博主作品列表和评论数据获取。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

短视频运营、品牌团队和内容分析人员可用它检索抖音公开视频与图文、查看热点和账号作品，并分析单条作品及评论，以支持选题、竞品研究和舆情观察。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Query keywords and links are sent to the third-party data service, and saved results may contain public user identifiers and comments.

Mitigation: Use a dedicated API token, review the provider's fees and data practices, and delete unneeded result files from logs/.

Risk: The external data service was not live-tested, so availability and returned data quality are not established by the source review.

Mitigation: Check the returned status and data before relying on results, and treat analysis of small comment samples as limited evidence.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/douyin-comments-assistant)
- [Publisher profile](https://clawhub.ai/user/why20261)
- [GuaiKei service and token access](https://www.guaikei.com)
- [Usage options](artifact/references/options.md)
- [Comment demand-mining guidance](artifact/references/demand-mining.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Files]

**Output Format:** [Structured JSON results, with optional concise analysis for the requested research task.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are written to local JSON files for search, creator posts, comments, and work details; hot-list results are returned directly. Retrieval limits depend on the token plan.]

## Skill Version(s):

1.4.2 (source: artifact/SKILL.md frontmatter, artifact/package.json, artifact/references/changelog.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
