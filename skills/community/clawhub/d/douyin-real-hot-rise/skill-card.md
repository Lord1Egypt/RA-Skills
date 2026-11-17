## Description:

查询抖音公开热榜、关键词搜索、创作者作品、作品详情与评论，并以结构化数据支持短视频趋势、竞品与评论分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

短视频运营人员、内容策划者与分析师可用它查询抖音公开趋势、内容和评论数据，辅助选题、竞品分析及舆情或需求归纳。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided search terms and Douyin links are sent to the GUAIKEI third-party data API.

Mitigation: Tell the user before sending their input, and send only the query or link needed for the requested lookup.

Risk: ClawScan reports an additional post-detail lookup beyond declared capabilities, partial code inspection, and unclear runtime environment access.

Mitigation: Review the detail lookup and runtime access before installation; avoid supplying sensitive input.

Risk: The skill requires a GUAIKEI API token, which should remain secret.

Mitigation: Store the token in a protected environment variable and do not include it in prompts or shared logs.

## Reference(s):

- [GUAIKEI service and setup](https://www.guaikei.com)
- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyin-real-hot-rise)
- [Options and limits](artifact/references/options.md)
- [Comment analysis guide](artifact/references/demand-mining.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON data; concise Markdown analysis or guidance when summarizing results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result availability and count depend on the query and API plan; the skill documents empty-result responses and per-plan limits.]

## Skill Version(s):

1.4.2 (source: release evidence, SKILL.md, package.json, changelog dated 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
