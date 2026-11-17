## Description:

中国城市天气查询工具

This skill is ready for commercial/non-commercial use.

## Publisher:

[woodcoal](https://clawhub.ai/user/woodcoal)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Chinese city and county-level weather questions, including current-day conditions, seven-day forecasts, rain likelihood, temperature, wind, and optional life indices.

### Deployment Geography for Use:

Global; the weather coverage is focused on Chinese cities and county-level regions.

## Known Risks and Mitigations:

Risk: City queries are sent to third-party weather services, and newly discovered city-code mappings may be cached locally in citys.txt.

Mitigation: Use only locations suitable for third-party lookup and local caching; review or clear citys.txt when location history should not persist.

Risk: Weather data can be delayed, and life indices are general-purpose guidance.

Mitigation: Treat outputs as informational and verify time-sensitive or safety-critical decisions with authoritative weather sources.

## Reference(s):

- [中国天气网](https://www.weather.com.cn/)
- [ClawHub skill page](https://clawhub.ai/woodcoal/skills/china-weather-skill)
- [Referenced China Weather skill](https://clawhub.ai/hoopan007/weather-china)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON weather forecast output, with documented shell command fallbacks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include seven-day forecasts, today's forecast only, and optional life indices such as clothing, car wash, and UV guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
