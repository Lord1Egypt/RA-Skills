## Description:

抖音公开数据智能获取工具。支持抖音关键词搜索、抖人作品抓取、获取作品评论、实时热榜跟踪，适用于短视频营销、竞品分析、舆情分析和热点监控，助力爆款内容策划与流量追踪。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users such as short video marketers, analysts, and creators can retrieve public Douyin video, account, comment, and trending data for topic research, competitor analysis, and sentiment review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplied links or video IDs are sent to a third-party API when the skill runs.

Mitigation: Review the links and IDs before execution and use the API only when that data sharing is acceptable.

Risk: Security review coverage is partial, with some components only partly analyzed.

Mitigation: Review the skill before installation, as advised by the security assessment.

## Reference(s):

- [Options and command parameters](artifact/references/options.md)
- [Output contract and JSON shapes](artifact/references/contract.md)
- [Errors and retry guidance](artifact/references/errors.md)
- [Demand mining guide](artifact/references/demand-mining.md)
- [Customer acquisition guide](artifact/references/customer-acquisition.md)
- [GuaiKei API and token information](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Analysis]

**Output Format:** [Structured JSON results from CLI queries, with Markdown usage and analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GUAIKEI_API_TOKEN; retrieves public Douyin data through the GuaiKei API.]

## Skill Version(s):

1.5.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
