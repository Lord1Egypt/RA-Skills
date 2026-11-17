## Description:

使用百度地图Web服务API进行地点搜索、天气查询、路线规划和地理编码。

This skill is ready for commercial/non-commercial use.

## Publisher:

[coreyleung-art](https://clawhub.ai/user/coreyleung-art)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to let an agent answer location-related requests with Baidu Maps Web Service API capabilities, including place search, weather lookup, route planning, geocoding, administrative district lookup, and IP location lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Map searches, addresses, coordinates, route endpoints, and IP lookup data may be sent to Baidu.

Mitigation: Use the skill only when sharing that location data with Baidu is acceptable for the user and use case.

Risk: Documented curl examples include user-supplied values in URL query parameters.

Mitigation: Use parameter-safe URL encoding through a structured HTTP client or carefully encoded curl requests instead of pasting raw user text into commands.

Risk: The Baidu Maps access key can be misused if exposed or overly broad.

Mitigation: Restrict the key by API, quota, and allowed usage where possible, and keep BAIDU_MAP_AK out of logs and shared outputs.

## Reference(s):

- [Baidu Maps Open Platform](https://lbsyun.baidu.com/)
- [ClawHub skill page](https://clawhub.ai/coreyleung-art/skills/baidu-map-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses from Baidu Maps endpoints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a BAIDU_MAP_AK environment variable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
