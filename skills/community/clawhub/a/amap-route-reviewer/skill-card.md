## Description: <br>
派出四位性格迥异的虚拟体验官，基于高德路径规划、天气和 POI 数据，用不同性格视角评价路线或旅行方案，帮助用户比较选择。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qhvssonic](https://clawhub.ai/user/qhvssonic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel planners use this skill to compare commuting routes, trip itineraries, or competing travel preferences through data-grounded persona reviews. The agent generates candidate plans, asks users to assign reviewer personas, and returns concise plain-text group-chat evaluations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route and travel recommendations can be misleading if source map, weather, POI, or traffic data is unavailable, outdated, or incomplete. <br>
Mitigation: Review important routes against current AMap data and local conditions before relying on the recommendation. <br>
Risk: The skill depends on `amap-lbs-skill` and the `AMAP_WEBSERVICE_KEY` environment variable for route and place data. <br>
Mitigation: Confirm the dependency is installed and the environment variable is configured before use. <br>


## Reference(s): <br>
- [Route Scouts ClawHub release](https://clawhub.ai/qhvssonic/amap-route-reviewer) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text group-chat style route and itinerary evaluations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include route summaries, persona-specific reviews, ratings, practical cautions, and an overall recommendation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
