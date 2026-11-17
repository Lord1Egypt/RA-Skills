## Description:

中国高速路线规划助手，智能利用各地绕城高速免费政策为车主省钱

This skill is ready for commercial/non-commercial use.

## Publisher:

[liumeixin](https://clawhub.ai/user/liumeixin)

### License/Terms of Use:

MIT-0

## Use Case:

Drivers and route-planning agents use this skill to plan China highway trips, compare toll costs, account for local plate-region restrictions, and identify toll-saving options from city ring-road free policies.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Route planning may involve addresses or coordinates, vehicle plate region, Amap API requests, and local toll or restriction context.

Mitigation: Ask only for route and plate-region details needed for the request, store the Amap key in an environment variable, and avoid collecting a full plate number unless a specific restriction query requires it.

Risk: Highway toll-free and traffic restriction policies can change after cached or documented values.

Mitigation: Check current policy information before presenting savings or restriction guidance, especially when cached policy data is older than one month.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liumeixin/skills/china-highway-route)
- [Amap geocoding API endpoint](https://restapi.amap.com/v3/geocode/geo?address={address}&key={API_KEY})
- [Amap driving route API endpoint](https://restapi.amap.com/v3/direction/driving?origin={origin}&destination={destination}&key={API_KEY})
- [Amap waypoint driving route API endpoint](https://restapi.amap.com/v3/direction/driving?origin={origin}&destination={destination}&waypoints={waypoints}&key={API_KEY})

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown route plan with route segments, toll estimates, restriction notices, savings comparison, and navigation links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Amap navigation links and policy-cache-informed toll-free route recommendations.]

## Skill Version(s):

1.0.6 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
