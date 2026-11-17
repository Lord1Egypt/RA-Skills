## Description:

B站评论分析工具用于根据B站视频链接或BV号获取一级评论，分页展示评论数据，进行积极、负面、需求和竞品四维分析，并生成可离线保存的交互式HTML报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, UP owners, brand operators, content planners, and product managers use this skill to retrieve Bilibili first-level comments, review audience sentiment, identify requests or competitor signals, and produce shareable HTML comment reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bilibili video identifiers are sent through RedFox APIs during comment retrieval.

Mitigation: Use the skill only for videos and workflows where sending the identifier to RedFox is acceptable, and confirm REDFOX_API_KEY scope and revocation options before use.

Risk: Generated HTML reports may contain commenter metadata, API-supplied URLs, external font loading, and AI-generated summaries.

Mitigation: Review generated reports locally before opening broadly or sharing, and avoid publishing reports that contain sensitive commenter metadata or unsanitized generated content.

## Reference(s):

- [Core Workflow](references/core_workflow.md)
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/bilibili-comment)
- [RedFox Hub API keys](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, HTML files, analysis]

**Output Format:** [Markdown responses with tables and analysis, JSON from helper scripts, and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY. The workflow fetches one Bilibili comment page per request and generates an HTML report for the current page.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
