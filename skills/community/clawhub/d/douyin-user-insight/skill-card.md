## Description:

基于抖音公开内容与互动数据，帮助产品、营销和内容团队识别用户需求、分析热点与竞品，并将洞察转化为产品机会。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

面向产品、营销与内容运营人员，用于新品开发、选题策划或品类进入前研究抖音公开内容和评论，整理用户诉求、竞品表现与潜在机会。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research keywords and links are sent to the third-party API at www.guaikei.com; its remote behavior and data retention were not verified.

Mitigation: Tell users what will be sent before querying, check the provider's billing and privacy terms, and use only the query details needed for the task.

Risk: The API token is required to access the service.

Mitigation: Keep GUAIKEI_API_TOKEN private and do not include it in prompts, reports, or shared logs.

Risk: Query results are saved locally and may contain research keywords, links, or public content used in analysis.

Mitigation: Review files in logs/ before sharing them and remove saved results when they are no longer needed.

Risk: Public platform data and comment samples may not represent the wider audience or establish a reliable market conclusion.

Mitigation: State the sample size and limits, and treat product opportunities as hypotheses that need independent validation.

## Reference(s):

- [ClawHub release](https://clawhub.ai/why20261/skills/douyin-user-insight)
- [Demand mining guide](references/demand-mining.md)
- [Command options](references/options.md)
- [Release changelog](references/changelog.md)
- [API provider and token setup](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON query results with concise written analysis and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query results may also be saved as JSON files in logs/; some playback and share URLs may expire.]

## Skill Version(s):

1.4.2 (source: release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
