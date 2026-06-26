## Description: <br>
查询北京花粉实时监测和预报数据，生成包含区级浓度、站点趋势、总量预报与分类预报的结果。北京 16 个固定站点，每区一个，用区名指定。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruochenlyu](https://clawhub.ai/user/ruochenlyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query Beijing district-level pollen readings, station trends, and forecasts. It can also generate daily pollen briefings for Beijing districts in JSON or readable text form. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to the documented Beijing pollen API when users ask about Beijing pollen conditions. <br>
Mitigation: Use it for Beijing pollen queries only, and review implicit invocation settings if calls should require explicit confirmation. <br>
Risk: Pollen readings and forecasts can be unavailable, delayed, or empty if the upstream public API fails or has no current data. <br>
Mitigation: Check the returned ok, warnings, and error fields before relying on the result or sending a daily briefing. <br>


## Reference(s): <br>
- [北京花粉监测 API 约定](references/api-contract.md) <br>
- [Beijing public pollen API](https://pollenwechat.bjpws.com) <br>
- [ClawHub skill page](https://clawhub.ai/ruochenlyu/beijing-pollen-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON, with optional human-readable text in data.text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, and jq; supports report, overview, stations, history, forecast, and daily query modes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
