## Description:

Tell the agent where you are and how far you want to walk, and it plans a walking route through nearby parks, lakesides, cafes, and similar points of interest with an Amap QR code for navigation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[770600682-cyber](https://clawhub.ai/user/770600682-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

External users ask the agent to plan city walks, casual runs, dog walks, or family strolls from a starting location and desired distance. The skill helps produce route summaries, suggested stops, weather-aware tips, and a QR code that opens the route in Amap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Locations or addresses provided by users are sent to Amap APIs for geocoding, place search, weather lookup, walking-route calculation, and QR-code route generation.

Mitigation: Use approximate starting points when location privacy matters, and install the skill only when this data sharing is acceptable.

Risk: The skill requires an AMAP_API_KEY credential.

Mitigation: Protect AMAP_API_KEY like any other API credential and avoid exposing it in prompts, logs, or shared outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/770600682-cyber/skills/amap-walk-route)
- [Amap Open Platform](https://lbs.amap.com)
- [Amap Web Service API Documentation](https://lbs.amap.com/api/webservice/summary)
- [Amap REST API Endpoint](https://restapi.amap.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown route summaries with structured stop lists, travel estimates, tips, and Amap QR-code navigation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AMAP_API_KEY and sends provided locations or addresses to Amap APIs for route planning.]

## Skill Version(s):

1.0.0 (source: server evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
