## Description:

根据用户输入的关键词调用 Redfox 接口搜索 Bilibili 最新视频，并支持排序、发布时间筛选、分页浏览和每日订阅提示。

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Bilibili creators, operators, data analysts, brands, and MCNs use this skill to research keyword-specific videos, monitor topic trends, compare content performance, and receive daily keyword updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Bilibili search terms to RedFox using REDFOX_API_KEY.

Mitigation: Install only after confirming the RedFox API key source, scope, validity, reset process, and acceptable data sharing.

Risk: The skill encourages daily keyword subscriptions that may create persistent scheduled tasks.

Mitigation: Require explicit keyword-bound confirmation before enabling a subscription, and make sure the user can list, disable, and delete the scheduled task.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/bilibili-keywords-search)
- [RedFox API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFox Bilibili Search API Endpoint](https://redfox.hk/story/api/bili/search)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown tables and concise text with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include video titles, authors, engagement counts, links, publish times, covers, tags, category labels, paging status, filter labels, and subscription guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
