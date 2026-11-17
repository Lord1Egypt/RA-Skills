## Description:

A skill to interact with Gaode Map (AMap) for location search and route planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[279458179](https://clawhub.ai/user/279458179)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search for places, geocode addresses, and plan driving, walking, bicycling, or transit routes through Gaode Map (AMap).

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Map searches, addresses, and route endpoints are sent to AMap.

Mitigation: Use the skill only when sharing that location data with AMap is acceptable.

Risk: The skill requires an AMap API key.

Mitigation: Prefer AMAP_API_KEY over the --key option, restrict the key where possible, and avoid exposing it in command history or logs.

Risk: The Python dependency is declared without a pinned version.

Mitigation: Pin or review the requests dependency before production deployment.

## Reference(s):

- [AMap Console](https://console.amap.com/)
- [AMap REST API](https://restapi.amap.com/v3)
- [ClawHub Skill Page](https://clawhub.ai/279458179/skills/gaodemapskill)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON responses from the AMap tool]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AMAP_API_KEY value and sends map queries, addresses, and route endpoints to AMap.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
