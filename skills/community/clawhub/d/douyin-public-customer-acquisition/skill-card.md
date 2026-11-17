## Description:

只读检索抖音公开视频、用户、作品详情、评论和热榜数据，并输出结构化 JSON，支持内容分析、需求挖掘和公域获客。

This skill is ready for commercial/non-commercial use.

## Publisher:

[um-why](https://clawhub.ai/user/um-why)

### License/Terms of Use:

MIT

## Use Case:

运营、增长和内容分析人员可用该技能检索抖音公开内容与账号数据，整理热点、竞品、评论诉求或潜在线索，并以 JSON 或简明分析报告供后续工作使用。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Douyin links may be sent to the third-party Guaikei service for lookup.

Mitigation: Use only public content and avoid confidential search terms or sensitive URLs; review the service's privacy and usage terms.

Risk: Public comment data could be reused as lead information or distributed beyond the documented internal-use scope.

Mitigation: Keep use within the documented personal or team scope, do not invent private contact details, and avoid improper distribution.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/um-why/skills/douyin-public-customer-acquisition)
- [Guaikei service and access support](https://www.guaikei.com)
- [Customer acquisition guide](references/customer-acquisition.md)
- [Demand mining guide](references/demand-mining.md)
- [Request routing guide](references/routing.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON data with concise Markdown summaries or tables when analysis is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Douyin data only; result fields vary by search, account, work-detail, comment, and trending query.]

## Skill Version(s):

1.5.0 (source: server-resolved release metadata and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
