## Description:

城市踏勘官 CityScout：把城市片区、任务目标和时间预算转成可执行的踏勘路线、观察清单、风险点和汇报摘要。适用于城市更新、商业选址、文旅动线、街区活力评估等需要地图能力和现场判断结合的任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kue0000](https://clawhub.ai/user/kue0000)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as urban researchers, planners, consultants, and commercial location teams use this skill to turn a city area, fieldwork goal, time budget, and travel mode into an actionable site-visit route, observation checklist, risk notes, photo plan, and short reporting summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location queries may be sent to Amap when the skill is used with real API access.

Mitigation: Review location-data handling requirements before enabling live API access and avoid sending sensitive site, user, or client information unless authorized.

Risk: Routes generated without API access may be mock or demo plans.

Mitigation: Verify route feasibility, POI details, weather, and safety assumptions with authoritative map data before submission or fieldwork.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kue0000/skills/city-scout-amap-skill)
- [Publisher profile](https://clawhub.ai/user/kue0000)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with route tables, checklists, risk notes, and summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May label routes as demo plans when live Amap API access is unavailable; real fieldwork outputs should distinguish evidence, inference, and uncertainty.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
