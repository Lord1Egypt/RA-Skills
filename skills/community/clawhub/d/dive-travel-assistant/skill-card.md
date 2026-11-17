## Description:

潜水旅行助手为潜水旅行者提供潜点搜索、考证指南、安全检查以及潜水目的地机票、酒店、交通和美食查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to plan recreational dive trips, compare dive destinations, review certification and safety guidance, and retrieve travel options for dive itineraries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dive travel search details such as origins, destinations, dates, hotel stays, and location searches are sent to the skill's cloud proxy services.

Mitigation: Use the skill only when sharing those itinerary and location details with the proxy services is acceptable.

Risk: If PROXY_TOKEN is set in the environment, the script uses it for proxy authentication.

Mitigation: Set PROXY_TOKEN only in environments where that credential is intended for this skill's proxy services.

Risk: Dive safety and certification information may be incomplete for a user's health status, training, local conditions, or dive plan.

Mitigation: Treat safety and certification output as planning guidance and confirm decisions with qualified dive professionals or medical experts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/dive-travel-assistant)
- [Publisher profile](https://clawhub.ai/user/travel-skills)

## Skill Output:

**Output Type(s):** [text, json, guidance, api calls]

**Output Format:** [JSON strings and concise text guidance returned by tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns local dive reference data and may include booking, route, hotel, restaurant, or error details from external travel proxy services.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
