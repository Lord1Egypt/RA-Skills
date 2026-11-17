## Description:

Map and location services for search, routing, and visualization, including geocoding, POI search, route planning, and heatmap generation capabilities.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[ayalnova](https://clawhub.ai/user/ayalnova)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to generate map search links, plan routes, find nearby places, and create heatmap links from location data. Some geocoding, route, POI, and travel planning workflows require the user's own map service API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill declares broad shared OpenClaw credential file locations while only requiring one map service API key.

Mitigation: Provide only AMAP_WEBSERVICE_KEY through a scoped environment variable or a dedicated credentials file containing only the map service key.

Risk: Location, routing, POI, or travel planning requests may be sent to the user's map service provider APIs.

Mitigation: Review provider terms and avoid submitting sensitive location data unless that use is appropriate for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ayalnova/skills/amap-integration)
- [AMap search](https://www.amap.com/search?query={keywords})

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with map links, route or search guidance, JSON data examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Selected workflows require AMAP_WEBSERVICE_KEY supplied by the user.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
