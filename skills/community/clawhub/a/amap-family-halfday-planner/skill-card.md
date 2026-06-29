## Description: <br>
亲子半日游规划师。输入出发地、孩子年龄、出行方式和家庭需求，调用高德 Web 服务能力生成亲子友好的半日游路线故事、行程表、设施清单、风险提醒和步行负担评估。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dghutr](https://clawhub.ai/user/dghutr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and family travel planners use this skill to turn a starting location, child age range, travel mode, and family needs into a child-friendly half-day itinerary. It uses Amap Web Service APIs to find nearby POIs, estimate walking legs, and produce route stories, schedules, preparation notes, risk reminders, and map capability notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route-planning details are sent to Amap Web Service APIs. <br>
Mitigation: Use the skill only when sharing the trip location and family route preferences with Amap is acceptable. <br>
Risk: Exact home addresses or sensitive family details could be exposed through route inputs, logs, or screenshots. <br>
Mitigation: Prefer nearby landmarks over exact home addresses, avoid unnecessary sensitive details, and rotate the Amap key if it is exposed. <br>
Risk: Generated family itineraries can be affected by incomplete or changing local conditions such as weather, crowds, closures, or facility availability. <br>
Mitigation: Review the itinerary before departure and check weather, hours, closures, and safety conditions in a current map or venue source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dghutr/amap-family-halfday-planner) <br>
- [Amap Open Platform](https://lbs.amap.com/) <br>
- [Demo preview](https://clawhub.ai/api/v1/skills/amap-family-halfday-planner/file?path=assets%2Fdemo-amap-real.svg&version=1.0.10) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown itinerary with route story, schedule table, preparation checklist, risk reminders, and Amap capability notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and an AMAP_API_KEY or AMAP_WEBSERVICE_KEY environment variable; sends route-planning inputs to Amap Web Service APIs.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
