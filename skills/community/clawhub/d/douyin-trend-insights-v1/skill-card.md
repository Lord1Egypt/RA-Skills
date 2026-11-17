## Description:

抖音趋势洞察帮助内容运营与分析人员检索抖音公开视频、热榜、作品和评论数据，并用于选题、竞品及舆情分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content operators and analysts use the skill to retrieve public Douyin video, creator, hot-list and comment data for trend tracking, content planning, competitor monitoring and sentiment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Douyin links supplied by the user are sent to the third-party Guaikei API.

Mitigation: Review the data-sharing disclosure and run the skill only when sending those inputs to the service is acceptable.

Risk: The security assessment was incomplete, so it does not establish that every component was fully reviewed.

Mitigation: Review the skill's behavior and disclosures before enabling it.

## Reference(s):

- [Usage options](references/options.md)
- [Comment demand analysis guide](references/demand-mining.md)
- [Release changelog](references/changelog.md)
- [Guaikei service and help](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON data with concise trend, content or comment analysis when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned fields depend on the selected query and public data availability; some video and share links may expire.]

## Skill Version(s):

1.4.2 (source: server release evidence, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
