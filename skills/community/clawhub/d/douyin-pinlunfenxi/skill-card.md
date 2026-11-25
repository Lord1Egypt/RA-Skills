## Description:

检索抖音公开视频、账号、作品和评论数据，并提供结构化结果，帮助分析评论反馈、内容趋势和用户需求。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content, marketing, and research teams can use the skill to explore public Douyin videos and creator accounts, inspect comments and engagement, and organize findings for trend, feedback, and demand analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports broader Douyin discovery and creator-data workflows in addition to comment analysis.

Mitigation: Review the available commands and use only the discovery or analysis steps relevant to the requested task.

Risk: Supplied keywords, video links, or IDs may be sent to the GUAIKEI service to retrieve public data.

Mitigation: Tell users which query or link will be sent and obtain their agreement before making the request.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/engheng-art/skills/douyin-pinlunfenxi)
- [GUAIKEI service](https://www.guaikei.com)
- [Usage and command guide](artifact/readme.md)
- [Output contract](artifact/references/contract.md)
- [Demand analysis guide](artifact/references/demand-mining.md)
- [Public audience research guide](artifact/references/customer-acquisition.md)
- [Command routing guide](artifact/references/routing.md)
- [Error handling guide](artifact/references/errors.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [Structured JSON results with concise analysis and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include public video, creator, engagement, and comment fields; requested keywords or video links are sent to GUAIKEI.]

## Skill Version(s):

1.4.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
