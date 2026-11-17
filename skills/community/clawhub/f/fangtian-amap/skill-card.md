## Description:

高德地图 API 调用工具，返回原始 JSON 数据。Use when users ask about 天气、地址、坐标、周边、路线、导航、打车、行程 in China.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangtianwd](https://clawhub.ai/user/fangtianwd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to query AMap for China-focused weather, geocoding, reverse geocoding, place search, POI detail, routing, distance, IP-location, navigation link, taxi link, and trip-planning responses.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Location, route, and IP-location queries are sent to AMap.

Mitigation: Avoid submitting sensitive home, workplace, route, or IP-location data unless sharing it with AMap is acceptable.

Risk: The installation instructions reference an `amap` executable that is not included in the artifact.

Mitigation: Confirm the executable source before installation and run standard local review or scanning before placing it on PATH.

Risk: The skill requires an AMap API key.

Mitigation: Set only `AMAP_API_KEY`, keep the key out of prompts and logs, and rotate it if it may have been exposed.

## Reference(s):

- [AMap API key console](https://console.amap.com/dev/key/app)
- [ClawHub skill page](https://clawhub.ai/fangtianwd/skills/fangtian-amap)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON responses and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and an AMAP_API_KEY environment variable; AMap API quotas and China-only service coverage apply.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
