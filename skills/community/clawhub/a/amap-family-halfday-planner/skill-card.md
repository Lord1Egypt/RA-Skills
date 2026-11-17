## Description:

亲子半日游规划师。输入出发地、孩子年龄、出行方式和家庭需求，调用高德 Web 服务能力生成亲子友好的半日游路线故事、行程表、设施清单、风险提醒和步行负担评估。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dghutr](https://clawhub.ai/user/dghutr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to plan child-friendly 3-5 hour outings from a given origin, age range, travel mode, and family preferences. It produces a route story, schedule, facilities checklist, risk reminders, walking burden estimate, and notes about the Amap Web Service capabilities used.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends entered origin, city, route preferences, and family needs to Amap Web Service APIs.

Mitigation: Use a scoped or quota-limited Amap API key and avoid entering precise home addresses or personal identifiers.

Risk: Route quality depends on Amap geocoding, POI search, walking-route data, and current local conditions.

Mitigation: Review the generated route before travel and check weather, business hours, crowding, closures, and safety constraints before departure.

## Reference(s):

- [Amap Open Platform](https://lbs.amap.com/)
- [ClawHub Skill Page](https://clawhub.ai/dghutr/skills/amap-family-halfday-planner)
- [Demo Preview](https://clawhub.ai/api/v1/skills/amap-family-halfday-planner/file?path=assets%2Fdemo-amap-real.svg&version=1.0.10)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with route summary tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and an AMAP_API_KEY or AMAP_WEBSERVICE_KEY environment variable to call Amap Web Service APIs.]

## Skill Version(s):

1.0.10 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
