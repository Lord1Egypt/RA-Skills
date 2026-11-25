## Description:

查询抖音公开视频、图文、达人作品、作品详情、评论和热榜数据，为市场趋势、选题与舆情分析提供结构化信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

内容运营、品牌与数据分析团队可用此技能检索抖音公开内容和账号数据，追踪热点、比较内容表现，并整理选题或舆情分析所需的信息。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and video or account identifiers are sent to a third-party API.

Mitigation: Avoid submitting sensitive terms or identifiers and confirm the service is approved for the data.

Risk: Account discovery and identifiable prospect collection can extend beyond market trend analysis.

Mitigation: Limit collection to the stated task, review the intended use, and handle results only within approved internal workflows.

Risk: The security scan had medium confidence and only partial inspection of executable files.

Mitigation: Review the source and security posture before installing or using the skill.

## Reference(s):

- [使用指南](readme.md)
- [输出契约](references/contract.md)
- [错误处理](references/errors.md)
- [需求挖掘指南](references/demand-mining.md)
- [服务与 API 访问](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Tables, Guidance]

**Output Format:** [Structured JSON with concise prose or tables for derived insights]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public content; results depend on available data and API plan limits. Requires Node.js and GUAIKEI_API_TOKEN.]

## Skill Version(s):

1.5.0 (source: server-resolved release, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
