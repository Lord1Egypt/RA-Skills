## Description:

抖音公开数据智能获取工具。用于抖音数据助手、抖音热榜、抖音数据分析、作品搜索、作品详情、评论分析、评论回复分析、达人数据、达人作品和达人短剧/合集。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Social media, marketing, and research teams can retrieve public Douyin videos, creator profiles, comments, and trending topics, then use the results for content planning, competitor analysis, audience feedback, and lead research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review warns that broad request routing may send unrelated requests to the external API and that some referenced code was only partially inspected.

Mitigation: Use the skill only for explicit Douyin public-data requests, review the keyword or URL before execution, and confirm you accept sending it to guaikei.com; inspect the remaining code before deployment.

## Reference(s):

- [Skill instructions](artifact/SKILL.md)
- [Output contract](artifact/references/contract.md)
- [Demand mining guide](artifact/references/demand-mining.md)
- [Public lead research guide](artifact/references/customer-acquisition.md)
- [Provider website](https://www.guaikei.com)
- [ClawHub release page](https://clawhub.ai/engheng-art/skills/douyin-shujuzhushou)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON results with concise text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public data; result fields vary by selected command.]

## Skill Version(s):

1.4.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
