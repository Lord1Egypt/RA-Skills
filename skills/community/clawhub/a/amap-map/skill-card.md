## Description:

Amap Map helps agents call the Gaode/Amap Web Service API for POI search, nearby search, POI detail lookup, route planning, geocoding, and reverse geocoding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[klscool](https://clawhub.ai/user/klscool)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to let an agent look up places, convert addresses and coordinates, and plan walking, bicycling, or driving routes through Amap/Gaode services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Map searches, addresses, coordinates, route endpoints, and the configured Amap API key are sent to Amap's web service.

Mitigation: Use the skill only when external Amap lookup is intended, avoid sensitive private locations, and manage the API key according to local credential-handling policy.

Risk: The skill writes aggregate local API call counts to a .usage.json file.

Mitigation: Review local workspace storage expectations and remove usage records when they are no longer needed.

## Reference(s):

- [Amap Open Platform](https://lbs.amap.com/)
- [Amap Web Service API endpoint](https://restapi.amap.com/v3)
- [Amap Developer Console](https://console.amap.com/)
- [ClawHub skill page](https://clawhub.ai/klscool/skills/amap-map)
- [Publisher profile](https://clawhub.ai/user/klscool)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON responses and Markdown usage guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Amap API key; local usage statistics are stored in a .usage.json file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
