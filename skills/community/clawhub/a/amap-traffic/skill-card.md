## Description:

高德地图实时路况查询与最优自驾路线规划技能。基于高德交通态势API和路径规划API，提供实时拥堵信息和最快路线建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[robin797860](https://clawhub.ai/user/robin797860)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query Amap traffic conditions, geocode route endpoints, and request driving-route recommendations that account for real-time congestion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Origin and destination addresses or coordinates are sent to Amap when the skill performs geocoding and route planning.

Mitigation: Avoid using the skill with highly sensitive precise locations unless sharing that data with Amap is acceptable.

Risk: The skill requires an Amap API key stored in OpenClaw configuration or an environment variable.

Mitigation: Protect the OpenClaw configuration file and rotate the API key if it may have been exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/robin797860/skills/amap-traffic)
- [Amap Open Platform](https://console.amap.com/)
- [Amap Geocoding API Endpoint](https://restapi.amap.com/v3/geocode/geo)
- [Amap Driving Route API Endpoint](https://restapi.amap.com/v3/direction/driving)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AMAP_KEY and sends location or route queries to Amap.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
