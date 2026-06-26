## Description: <br>
Didi Map JSAPI helps developers write, review, and debug code that uses Didi Map APIs for map initialization, markers, overlays, layers, events, controls, services, and performance-related implementation details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcmdhr](https://clawhub.ai/user/mcmdhr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill as reference guidance when integrating Didi Map JSAPI features, including map setup, secure key configuration, overlays, controls, vector layers, geolocation, geocoding, POI search, and route planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applications built from the location, routing, geocoding, or POI examples can process sensitive location or trip data. <br>
Mitigation: Add clear user consent, privacy notices, data minimization, logging limits, and regional compliance checks before shipping an app. <br>
Risk: Map service keys can be exposed if examples are copied into production without key protection. <br>
Mitigation: Use the documented proxy-server pattern or another server-side key protection approach, and avoid plaintext client-key configuration in production. <br>


## Reference(s): <br>
- [Didi Map JSAPI ClawHub Release](https://clawhub.ai/mcmdhr/didi-map-jsapi) <br>
- [Skill Overview](artifact/SKILL.md) <br>
- [JSAPI Authentication](artifact/references/jsapi-auth.md) <br>
- [Map](artifact/references/map.md) <br>
- [Marker](artifact/references/marker.md) <br>
- [Overlay Base](artifact/references/overlay-base.md) <br>
- [Vector Base Layer](artifact/references/vector-base-layer.md) <br>
- [Geolocation](artifact/references/geolocation.md) <br>
- [Geocode Service](artifact/references/service-geocode.md) <br>
- [POI Service](artifact/references/service-poi.md) <br>
- [Route Planning Service](artifact/references/service-route.md) <br>
- [Type Definitions](artifact/references/types.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JavaScript, HTML, JSON, and Nginx configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; examples may require Didi Map service keys and production privacy controls before use in an application.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
