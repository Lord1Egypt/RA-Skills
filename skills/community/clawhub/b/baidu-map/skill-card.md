## Description:

Baidu Map helps agents use a zero-dependency Baidu Maps Web API CLI for geocoding, POI search, routing, coordinate conversion, and BD-09 coordinate-system guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Baidu Maps Web Service APIs, normalize addresses or POI data, troubleshoot BD-09/WGS-84/GCJ-02 coordinate issues, and prepare CLI commands or implementation guidance for map workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Map queries, addresses, coordinates, route endpoints, and generic call parameters are sent to Baidu Maps APIs.

Mitigation: Use only data approved for Baidu Maps processing and avoid submitting sensitive locations unless that data sharing is acceptable.

Risk: The generic call command can access additional Baidu endpoints and may consume API quota.

Mitigation: Review the endpoint and parameters before execution, scope the Baidu Maps AK appropriately, and monitor quota usage.

Risk: Baidu Maps defaults to BD-09 and coordinate order differs across commands, which can cause inaccurate locations if mixed with WGS-84 or GCJ-02 data.

Mitigation: Confirm coordinate system and latitude/longitude order before storing or displaying results, and use conversion steps where required.

## Reference(s):

- [Baidu Map ClawHub skill page](https://clawhub.ai/zhangifonly/skills/baidu-map)
- [Baidu Maps API endpoint](https://api.map.baidu.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a Baidu Maps server-side AK and can consume Baidu Maps API quota.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
