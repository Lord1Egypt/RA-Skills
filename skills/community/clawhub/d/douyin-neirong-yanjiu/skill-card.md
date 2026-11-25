## Description:

抖音公开数据智能获取工具。当用户需要做抖音内容研究、抖音选题、热点观察、竞品内容对比、趋势判断、评论洞察或创作者资料整理时使用。面向内容运营、品牌调研和创作者。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators, brand researchers, and creators use this skill to retrieve public Douyin video, account, comment, and trending-topic data for topic planning, trend research, competitor comparisons, and audience insight.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplied video links or IDs are sent to an external API.

Mitigation: Use the skill only if you are comfortable sharing those identifiers with the provider.

Risk: Inspection covered only part of the skill files, leaving some behavior unverified.

Mitigation: Review the skill before installation; the benign verdict has medium confidence and is not a safety guarantee.

## Reference(s):

- [GuaiKei API access and support](https://www.guaikei.com)
- [Output contract](references/contract.md)
- [Error handling](references/errors.md)
- [Demand mining guide](references/demand-mining.md)
- [Customer acquisition guide](references/customer-acquisition.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON data with optional text or Markdown summaries and analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries cover public Douyin data and require a GuaiKei API token; returned media links may expire.]

## Skill Version(s):

1.4.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
