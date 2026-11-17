## Description:

专注于获取抖音最新的热榜数据，每小时更新，包含热点事件、热度值和跳转链接；支持查询近7天、近30天历史热榜，并支持订阅定时推送。

This skill is ready for commercial/non-commercial use.

## Publisher:

[if530770](https://clawhub.ai/user/if530770)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, MCN operations teams, brand marketers, and short-video operators use this skill to query current and recent Douyin hot trends, compare trend movement, and generate creator-oriented content guidance and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a REDFOX_API_KEY and sends that key to redfox.hk.

Mitigation: Use a narrowly scoped, revocable key; set it as an environment variable; and avoid placing it in prompts, logs, generated files, or source code.

Risk: The skill can read shell startup files while looking for REDFOX_API_KEY.

Mitigation: Review before installing and prefer environment-only key configuration instead of storing credentials in shell startup files.

Risk: The skill writes local JSON, HTML, and PDF report artifacts.

Mitigation: Review generated artifacts before sharing them and remove any files that contain sensitive or unwanted trend data.

Risk: Generated HTML reports can execute JavaScript from embedded data and cdnjs when opened.

Mitigation: Open generated reports only in a controlled browser context and review report contents before distribution.

## Reference(s):

- [Agent execution workflow](references/core_workflow.md)
- [RedFoxHub](https://redfox.hk/)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFoxHub Douyin hotspot API endpoint](https://redfox.hk/story/api/hotSpot/getListByPlatform)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown trend tables and guidance, JSON API data, and generated HTML/PDF report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a REDFOX_API_KEY and may create local JSON, HTML, and PDF report artifacts.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
