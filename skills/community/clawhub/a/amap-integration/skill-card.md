## Description: <br>
Map and location services for search, routing, and visualization. Provides geocoding, POI search, route planning, and heatmap generation capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayalnova](https://clawhub.ai/user/ayalnova) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to generate map search links, plan routes, look up nearby places, and create location-based visualizations with optional map-service API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map queries, route requests, and submitted location data may reveal sensitive home, work, or travel locations to the map provider. <br>
Mitigation: Avoid submitting sensitive locations unless sharing them with the provider is acceptable. <br>
Risk: User-provided map-service API keys can consume provider quota or incur account-level usage exposure. <br>
Mitigation: Use a dedicated API key where possible and monitor provider quota and usage. <br>


## Reference(s): <br>
- [Map Integration Service on ClawHub](https://clawhub.ai/ayalnova/amap-integration) <br>
- [AMap Search](https://www.amap.com/search?query={keywords}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with links, configuration instructions, and optional JSON data examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include URLs to map-provider services and setup guidance for user-provided API keys.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
