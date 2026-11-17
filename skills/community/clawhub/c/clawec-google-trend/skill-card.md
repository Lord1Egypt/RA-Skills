## Description:

通过 Clawec API 查询 Google Trends 关键词搜索热度与趋势，支持多词对比与按国家/地区筛选。在用户需要谷歌趋势、搜索热度对比、市场兴趣变化、关键词趋势调研、选品前需求验证时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and ecommerce operators use this skill to query Google Trends keyword interest through the ClawEC API, compare multiple keywords by region, and turn trend results into concise product-research observations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided search keywords and a Clawec API token to clawec.com.

Mitigation: Use only organization-approved accounts and avoid sensitive, proprietary, or personal search terms unless that data sharing is permitted.

Risk: Trend outputs can be mistaken for sales or demand data.

Mitigation: Label results as search interest and pair trend observations with separate market, conversion, and sales validation before making business decisions.

## Reference(s):

- [Google Trend response schema](references/response-schema.md)
- [ClawEC API base URL](https://www.clawec.com/api)
- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-google-trend)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Chinese Markdown trend summary with optional tables and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries depend on the ClawEC API response and should state that search interest is not sales volume.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
