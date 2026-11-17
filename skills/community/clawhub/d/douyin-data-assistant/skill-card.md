## Description:

检索抖音公开内容与热榜，获取作品、创作者及评论数据，并支持短视频选题、竞品监控和舆情分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

短视频运营者、内容分析人员和品牌团队可用它搜索抖音公开视频与图文、查看热榜和创作者作品，并分析单条作品及评论，为选题、竞品监控和舆情分析提供数据。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided keywords and Douyin links or IDs to the third-party API at guaikei.com.

Mitigation: Before execution, make sure the user understands this disclosure; use the skill only for public Douyin content.

Risk: The security assessment is benign but has medium confidence because inspection was partial and tool-misuse analysis was degraded; tool scope remains unclear.

Mitigation: Review each documented command against the requested task and run only the command needed for that task.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/douyin-data-assistant)
- [Publisher profile](https://clawhub.ai/user/why20261)
- [API access and support](https://www.guaikei.com)
- [Usage options](references/options.md)
- [Comment analysis guide](references/demand-mining.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON, with concise text analysis when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public-content data; results and request limits depend on the selected limit and token plan.]

## Skill Version(s):

1.4.2 (source: SKILL.md frontmatter, changelog, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
