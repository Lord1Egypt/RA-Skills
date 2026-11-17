## Description:

查询中国多地公交线路、站点、车辆位置及实时到站信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[houxingze0902](https://clawhub.ai/user/houxingze0902)

### License/Terms of Use:

MIT-0

## Use Case:

旅客和出行助手可查询公交线路、附近站点、车辆位置和预计到站时间，辅助规划出行。

### Deployment Geography for Use:

China (supported cities)

## Known Risks and Mitigations:

Risk: Running an unpinned external npm transit server with local user privileges.

Mitigation: Review the package before installation, pin a reviewed exact version, and prefer scoped native MCP registration where available.

Risk: Route, stop, city, and coordinate queries are sent to the transit service.

Mitigation: Avoid submitting sensitive location details and disclose the data sharing to users.

## Reference(s):

- [chelaile-bus on ClawHub](https://clawhub.ai/houxingze0902/skills/chelaile-bus)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown with bus arrival details and optional command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Arrival estimates may be unavailable for vehicles beyond the nearest bus; vehicle data may lag by 1–2 minutes.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence and scripts/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
