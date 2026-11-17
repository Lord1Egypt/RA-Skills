## Description:

查询北京花粉实时监测和预报数据，生成包含区级浓度、站点趋势、总量预报与分类预报的结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruochenlyu](https://clawhub.ai/user/ruochenlyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query Beijing district-level pollen conditions, trends, forecasts, and daily briefings. It supports human-readable reports and structured JSON for downstream automation.

### Deployment Geography for Use:

China (Beijing pollen data only)

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to the configured public Beijing pollen API host.

Mitigation: Deploy it only in environments where that outbound network access is allowed and expected.

Risk: The skill depends on bash, curl, and jq at runtime.

Mitigation: Verify those dependencies are installed before invoking the skill, and handle dependency errors returned by the script.

Risk: The skill is limited to Beijing pollen data and should not be used for other geographies.

Mitigation: Use district-scoped Beijing queries only, and route non-Beijing pollen requests to another source.

## Reference(s):

- [北京花粉监测 API 约定](references/api-contract.md)
- [ClawHub skill page](https://clawhub.ai/ruochenlyu/skills/beijing-pollen-monitor)
- [Upstream Beijing pollen API host](https://pollenwechat.bjpws.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON by default; human-readable text is returned inside data.text when text format is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, curl, and jq; makes outbound requests to the configured public Beijing pollen API host.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
