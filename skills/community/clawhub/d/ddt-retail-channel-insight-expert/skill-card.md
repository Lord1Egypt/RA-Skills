## Description:

零售渠道与竞对分析专家，分析便利店、超市、药店、美妆等连锁品牌的门店网络、业态分类、区域覆盖与品牌对比。适用于市场、渠道和竞争情报团队识别主力市场与增长空间。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

市场、渠道和竞争情报团队使用该技能分析已发布零售品牌的门店规模、业态结构、区域覆盖、城市排行和多品牌竞争差异。它适用于把聚合 API 数据转成渠道判断、候选点初筛和可验证的门店网络结论。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends retail brand names, optional coordinates, or public store IDs to the DDT retail analytics API.

Mitigation: Use it only for approved retail analysis workflows and avoid confidential location analyses unless the organization permits that data flow.

Risk: A DDT_API_KEY is required for API calls.

Mitigation: Keep the API key in a local or controlled runtime environment and do not place real keys in skill files, chat transcripts, logs, or version control.

Risk: The skill is scoped to retail brands and limited public or restricted-preview data.

Mitigation: Stop rather than extrapolate when the requested industry, brand, coverage, or API response is outside the published retail data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-retail-channel-insight-expert)
- [DDT retail analytics API homepage](https://gotoshop-ai.com/ddtclaw/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with concise conclusions, key metrics, coverage notes, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses current API responses as the source for retail brand metrics and limits detailed store output to explicit user requests.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
