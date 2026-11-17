## Description:

智能通勤助手，实时查询驾车、公交、骑行、步行路线，结合天气和路况，推荐最优通勤方案并可生成高德导航二维码。

This skill is ready for commercial/non-commercial use.

## Publisher:

[f0ll0wwind](https://clawhub.ai/user/f0ll0wwind)

### License/Terms of Use:

MIT-0

## Use Case:

Commuters use this skill to compare driving, public transit, cycling, and walking options for daily trips, then choose a route based on travel time, weather, traffic, vehicle restrictions, and nearby services.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Amap receives route-query data such as addresses or coordinates during commute lookups.

Mitigation: Use only when that data sharing is acceptable, and avoid entering unnecessary personal details in location names.

Risk: The described commute_log.json can accumulate precise local commute history.

Mitigation: Make logging opt-in, minimize stored precision, set a retention period, and protect or delete the log when it is no longer needed.

Risk: The qrcode dependency is required for terminal navigation QR codes.

Mitigation: Pin the dependency version before regular use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/f0ll0wwind/skills/commute-survival-guide)
- [Amap Open Platform](https://lbs.amap.com/)
- [Amap Web Service API documentation](https://lbs.amap.com/api/webservice/summary)
- [Amap Direction API documentation](https://lbs.amap.com/api/webservice/guide/api/direction)
- [Amap Weather API documentation](https://lbs.amap.com/api/webservice/guide/api/weather)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style route comparisons, commute reports, configuration steps, and terminal QR-code guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Amap Web Service APIs and append local commute history to commute_log.json when used as described.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
