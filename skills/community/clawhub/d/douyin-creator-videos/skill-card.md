## Description:

该技能面向抖音公开内容，可按关键词检索视频与图文、查询热榜、查看单条作品和博主作品，并获取评论供内容分析，结果以结构化 JSON 输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

短视频运营、品牌与内容分析人员可用它检索抖音公开视频和图文、跟踪创作者作品与热点，并查看作品详情和评论。Agent 可基于结构化结果整理选题、竞品对比、发文节奏或评论观点摘要。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Douyin links are sent to the Guaikei third-party API.

Mitigation: Use public content only, confirm the user is authorized to share the query or link, and avoid sending confidential information.

Risk: The security assessment is partial: 24 of 42 components were scanned fully, 18 partially, and the tool-misuse analyzer was degraded; the benign verdict has medium confidence.

Mitigation: Consider this uncertainty before installing and review and scan the skill before use.

Risk: Release evidence lists the license as MIT-0, while artifact/SKILL.md and artifact/package.json state MIT.

Mitigation: Confirm which license applies to this release before redistributing it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/douyin-creator-videos)
- [Guaikei service](https://www.guaikei.com)
- [Usage options](references/options.md)
- [Comment analysis guide](references/demand-mining.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON with concise text summaries or analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can include author, interaction, timestamp, and media-link fields; some media links expire.]

## Skill Version(s):

1.4.2 (source: SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
