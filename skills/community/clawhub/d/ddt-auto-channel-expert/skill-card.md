## Description:

汽车后市场渠道洞察专家，分析润滑油、轮胎、维修保养和汽服连锁的门店规模、省市分布、服务类型与品牌对比，帮助市场、渠道和战略团队判断强弱市场与覆盖空白。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External market, channel, and strategy teams use this skill to analyze automotive aftermarket brand store networks, regional coverage, service categories, surroundings, and multi-brand channel competition. It is intended for published aggregate data and limited public store/location lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys could be exposed if copied into chats, logs, skill files, or version control.

Mitigation: Keep DDT_API_KEY in a controlled environment variable and never include real keys in outputs or stored artifacts.

Risk: API cost, quota, or availability issues could interrupt analysis.

Mitigation: Monitor API costs and limits, stop on authorization or balance failures, and report service request identifiers when upstream errors occur.

Risk: Sensitive location data could be submitted during nearby-store or site-screening lookups.

Mitigation: Avoid entering private or sensitive coordinates unless appropriate for the user's use case and data-handling requirements.

Risk: Limited previews, missing coverage, or unavailable historical open-close data could lead to overstated market conclusions.

Mitigation: Use returned coverage and preview fields, label unavailable coverage explicitly, and avoid trend or complete-market claims that are not present in API responses.

## Reference(s):

- [DDT automotive aftermarket API homepage](https://gotoshop-ai.com/ddtclaw/)
- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-auto-channel-expert)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise analytical summaries, key metrics, coverage notes, limited store details when requested, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should not include API keys, storage IDs, data suppliers, internal fields, or unsupported trend claims.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
