## Description:

帮助品牌、MCN、内容运营和创作者分析抖音公开内容、账号、评论与热点，并整理结构化数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

品牌、MCN、内容运营人员和创作者可用它搜索抖音视频、图文、账号、作品与评论，追踪热点并整理竞品、内容策略、舆情、需求或获客分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and supplied Douyin links or video IDs are sent to the third-party Guaikei API.

Mitigation: Avoid sending sensitive or confidential information, and review the provider's terms before use.

Risk: The documented lead analysis workflow identifies people from public comments.

Mitigation: Use results only for authorized internal analysis, do not infer private contact details, and do not automate unsolicited outreach.

## Reference(s):

- [Skill instructions](SKILL.md)
- [Output contract](references/contract.md)
- [Demand mining guide](references/demand-mining.md)
- [Public lead analysis guide](references/customer-acquisition.md)
- [Guaikei service](https://www.guaikei.com)
- [ClawHub release](https://clawhub.ai/engheng-art/skills/douyin-data-insight)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Markdown]

**Output Format:** [Structured JSON results with concise summaries, tables, or reports for follow-up analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be empty; query limits and availability depend on the API plan.]

## Skill Version(s):

1.4.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
