## Description:

抖音公开数据智能获取工具。当需要抖音关键词搜索、抖人作品抓取、获取作品评论、实时热榜跟踪，短视频营销、竞品分析、舆情分析和热点监控，助力爆款内容策划与流量追踪时，请使用该技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External-facing creators, marketers, and analysts use this skill to find public Douyin videos and creators, review works and comments, and track trending topics for content planning, competitor research, and sentiment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked the skill suspicious with medium confidence, citing broad intent routing and incomplete inspection; this is a review warning and does not establish malicious behavior.

Mitigation: Review the source and scan warning before installation, and decide whether you are comfortable with the skill's Douyin data requests.

Risk: Running a query sends its keywords, links, or IDs to the Guaikei API service.

Mitigation: Use only query details that are appropriate to share with that third-party service, and get consent before submitting another person's provided links or IDs.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/engheng-art/skills/douyin-daren)
- [Guaikei service](https://www.guaikei.com)
- [Options and command parameters](references/options.md)
- [Output contract](references/contract.md)
- [Errors and retry guidance](references/errors.md)
- [Demand mining guidance](references/demand-mining.md)
- [Customer acquisition guidance](references/customer-acquisition.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON data with concise natural-language summaries and analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI responses use a consistent JSON envelope; non-hot query results can also be saved as local files.]

## Skill Version(s):

1.4.3 (source: server-resolved release metadata, changelog entry)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
