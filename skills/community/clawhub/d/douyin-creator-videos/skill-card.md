## Description:

搜索抖音公开视频和账号、查看创作者作品与详情、获取评论和热榜，并返回结构化数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, social media analysts, and marketing teams use it to research public Douyin videos, creator accounts, comments, and trends, then plan content or compare public engagement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a benign result with medium confidence, but 22 of 53 components were only partially inspected.

Mitigation: Review the skill files and account for the incomplete scan coverage before installation.

Risk: The skill includes keyword-based account discovery, and supplied links or IDs are sent to a third-party API.

Mitigation: Use account search intentionally and submit only public links or IDs you are comfortable sharing with the service.

## Reference(s):

- [Skill guide](artifact/SKILL.md)
- [Technical overview and command reference](artifact/readme.md)
- [Output contract](artifact/references/contract.md)
- [Error handling](artifact/references/errors.md)
- [Service and API access](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON results with concise analysis or guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the requested query and API plan; media and share URLs may expire.]

## Skill Version(s):

1.5.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
