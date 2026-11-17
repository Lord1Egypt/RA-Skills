## Description:

Amap Smart Route helps an agent plan real-time driving, walking, transit, and bicycling routes with estimated duration, distance, route options, and Amap navigation links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[770600682-cyber](https://clawhub.ai/user/770600682-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer route-planning questions such as how to travel between two places, how long a trip may take, and which travel mode or route option to choose. The skill is intended for workflows that can provide an Amap Web Service API key and can send origin and destination information to Amap for route calculation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an Amap API key.

Mitigation: Provide AMAP_API_KEY only in a trusted environment and avoid exposing it in prompts, logs, or shared outputs.

Risk: Route planning sends origin and destination addresses or coordinates to Amap.

Mitigation: Use the skill only when the user is comfortable sharing those route details with Amap, and avoid submitting unnecessary sensitive location information.

Risk: Ambiguous travel requests can produce incorrect routes or modes.

Mitigation: Confirm the exact origin, destination, and travel mode before allowing API calls for unclear requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/770600682-cyber/skills/amap-smart-route)
- [Amap Web Service API overview](https://lbs.amap.com/api/webservice/summary)
- [Amap geocoding API documentation](https://lbs.amap.com/api/webservice/guide/api/georegeo)
- [Amap route planning API documentation](https://lbs.amap.com/api/webservice/guide/api/newroute)
- [Amap developer console](https://console.amap.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Markdown route summaries with distances, durations, route options, and navigation links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AMAP_API_KEY and sends origin and destination data to Amap Web Service APIs.]

## Skill Version(s):

1.0.0 (source: evidence release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
