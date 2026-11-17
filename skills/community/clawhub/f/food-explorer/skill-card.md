## Description:

当用户想去某个地方吃饭、探店，或者询问附近有什么好吃的时使用。能根据用户位置、时间（早/中/晚）、口味偏好、预算推荐合适的餐厅。

This skill is ready for commercial/non-commercial use.

## Publisher:

[newobject11](https://clawhub.ai/user/newobject11)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get nearby restaurant recommendations from a location, meal timing, cuisine preference, and budget. It can query Baidu Maps for live place data and fall back to bundled city food data when the API is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided locations and restaurant preferences may be sent to Baidu Maps during geocoding and nearby search.

Mitigation: Use coarse locations where possible and disclose the external Baidu Maps lookup before sending sensitive location details.

Risk: A Baidu Maps API key is required for live search and could be exposed if hardcoded.

Mitigation: Store BAIDU_MAP_API_KEY in the environment or a secret manager and avoid embedding it in skill files or prompts.

Risk: The requests dependency is not version-pinned in the artifact metadata.

Mitigation: Pin and review dependency versions before production deployment.

Risk: Budget filtering is not a strict constraint in this version.

Mitigation: Treat budget values as guidance and verify price information before acting on a recommendation.

Risk: Restaurant data from Baidu Maps or the bundled fallback database may be stale.

Mitigation: Ask users to confirm business hours, availability, and queue conditions before visiting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/newobject11/skills/food-explorer)
- [Baidu Map API reference](references/baidu_map_api.md)
- [City food database reference](references/city_food_db.md)
- [Baidu Maps developer documentation](https://lbsyun.baidu.com/)
- [Baidu Maps geocoding guide](https://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding)
- [Baidu Maps place search guide](https://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown-style text with ranked restaurant recommendations and practical visit tips]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include restaurant names, ratings, prices, distance estimates, addresses, phone numbers, fallback recommendations, and reminders to confirm current details.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
