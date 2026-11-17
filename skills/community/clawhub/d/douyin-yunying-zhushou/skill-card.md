## Description:

面向抖音运营的数据工具，可搜索视频与图文、查看创作者作品和作品详情、读取评论及实时热榜，并返回结构化 JSON。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

抖音运营、内容策划和分析人员可用它研究选题与热点、查看公开作品表现、监测对标账号，并基于评论开展舆情或需求分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Douyin links are sent to the third-party GUAIKEI data service.

Mitigation: Confirm the user authorizes that data transfer and keep requests within the intended public-data scope.

Risk: The skill requires a GUAIKEI API token in an environment variable.

Mitigation: Restrict access to the token and keep it out of shared logs and outputs.

Risk: The security scan inspected only part of the bundled components, so it cannot rule out issues in partially inspected content.

Mitigation: Review and scan the remaining components before deployment.

Risk: Timestamps use Beijing time and may be misread in other time zones.

Mitigation: Convert timestamps to the intended local time zone before comparing events.

## Reference(s):

- [参数说明](references/options.md)
- [评论需求分析指南](references/demand-mining.md)
- [更新日志](references/changelog.md)
- [GUAIKEI 抖音运营助手](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON response envelope]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search, comment, and hot-list results are arrays; creator and single-work results are objects. Returned counts depend on the selected plan and request limit.]

## Skill Version(s):

1.4.2 (source: release evidence, SKILL.md, package.json, and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
