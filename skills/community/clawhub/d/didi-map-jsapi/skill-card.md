## Description:

Provides developer guidance for writing, reviewing, and debugging code that uses the DiDi Map JSAPI for map initialization, markers, overlays, layers, events, controls, and performance-related map integration tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcmdhr](https://clawhub.ai/user/mcmdhr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as reference material when integrating DiDi Map JSAPI features into web applications, including maps, markers, overlays, vector layers, controls, geolocation, routing, POI search, and geocoding. It is also useful when reviewing or debugging DiDi Map JSAPI usage for key handling, event behavior, and UI map interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples involving map, location, POI, route, or search data could expose user location data or search terms if copied into an application without privacy review.

Mitigation: Keep keys server-side, avoid logging raw coordinates or search terms, and require clear user consent for geolocation and continuous tracking.

Risk: Popup examples include HTML insertion patterns that may be unsafe with untrusted content.

Mitigation: Prefer text-safe popup APIs or sanitize HTML before using HTML-based popup content.

Risk: Proxy and credential examples may be insecure if deployed with plaintext transport or exposed client secrets.

Mitigation: Use HTTPS for proxy endpoints and route JSAPI requests through a server-side proxy instead of placing sensitive keys directly in web client code.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mcmdhr/skills/didi-map-jsapi)
- [Publisher Profile](https://clawhub.ai/user/mcmdhr)
- [DiDi Map Console Key Management](https://lbs.xiaojukeji.com/console/fe/managekey)
- [JSAPI Authentication](references/jsapi-auth.md)
- [Map](references/map.md)
- [Marker](references/marker.md)
- [Popup](references/popup.md)
- [Geolocation](references/geolocation.md)
- [Route Planning Service](references/service-route.md)
- [POI Search Service](references/service-poi.md)
- [Type Definitions](references/types.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JavaScript, HTML, and Nginx configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are developer reference responses and should be reviewed before production use, especially for key handling, location data, and HTML popup content.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
