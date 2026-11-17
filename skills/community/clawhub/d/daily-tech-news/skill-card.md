## Description:

每日科技资讯聚合。自动抓取GitHub Trending、51CTO、百度热搜科技榜，筛选AI/Cloud/ML领域内容，生成结构化简报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgugeng](https://clawhub.ai/user/lgugeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to gather Chinese-language AI and technology news, filter and deduplicate items, and generate structured daily briefings. It can also support scheduled report generation and optional Feishu delivery after local configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled execution and outbound Feishu delivery can publish generated reports without enough operator review.

Mitigation: Configure the webhook yourself, disable scheduled runs until reviewed, and require confirmation before pushes.

Risk: Weak date and report-file path handling can read or write unintended local JSON files.

Mitigation: Run the skill from a constrained working directory, validate date and report-file inputs, and fix TODAY/REPORT_FILE path handling before use in valuable workspaces.

Risk: Generated source claims and summaries may overstate verification or freshness.

Mitigation: Review generated summaries and original links before external publication, especially when source fetching fails or uses placeholder content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lgugeng/skills/daily-tech-news)
- [GitHub Trending](https://github.com/trending)
- [Baidu technology hot list](https://top.baidu.com/board?tab=realtime&category=tech)
- [机器之心](https://www.jiqizhixin.com/)
- [量子位](https://www.qbitai.com/)
- [InfoQ China](https://www.infoq.cn/)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown briefings, JSON daily reports, Feishu card payloads, and setup or run commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run on a daily schedule and may send reports to Feishu when a webhook is configured.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
