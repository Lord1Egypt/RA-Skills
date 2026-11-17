## Description:

Provides Baidu Maps JSAPI WebGL (BMapGL) development guidance for map initialization, overlays, layers, events, controls, route services, local search, geocoding, and coordinate conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wahddbing](https://clawhub.ai/user/wahddbing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill as a Baidu Maps JSAPI WebGL reference when writing, reviewing, or debugging web map code. It supports work involving map setup, overlays, event handling, style and layer configuration, routing, local search, geocoding, and coordinate conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-paste JavaScript examples may be used without security review in web pages.

Mitigation: Review generated code before use and adapt examples to the application's security standards.

Risk: Map tiles or scripts may be loaded with non-HTTPS URLs.

Mitigation: Prefer explicit HTTPS URLs for scripts, tiles, and other external map resources.

Risk: Untrusted content may be inserted into custom overlays or InfoWindow HTML.

Mitigation: Sanitize or escape untrusted data before placing it into innerHTML, custom overlay DOM, or InfoWindow content.

Risk: A Baidu Maps API key may be exposed or over-permissioned in browser code.

Mitigation: Restrict the Baidu Maps API key by origin, service scope, and quota before using it in generated integrations.

Risk: Address, route, geocoding, and coordinate lookups may process location data.

Mitigation: Provide appropriate privacy notice or consent before collecting or transmitting user location or address data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wahddbing/skills/bmap-jsapi-gl)
- [Baidu map style editor](https://lbsyun.baidu.com/apiconsole/custommap)
- [Base classes](references/base-classes.md)
- [Circle](references/circle.md)
- [Common constants](references/constants.md)
- [Coordinate conversion](references/convertor.md)
- [Custom overlay](references/custom-overlay.md)
- [Driving route](references/driving-route.md)
- [Geocoder](references/geocoder.md)
- [InfoWindow](references/info-window.md)
- [LocalSearch](references/local-search.md)
- [Map events](references/map-events.md)
- [Map initialization](references/map-init.md)
- [Map style](references/map-style.md)
- [Marker](references/marker.md)
- [MVTLayer](references/mvt-layer.md)
- [Overlay common operations](references/overlay-common.md)
- [Overlay events](references/overlay-events.md)
- [Polygon](references/polygon.md)
- [Polyline](references/polyline.md)
- [Riding route](references/riding-route.md)
- [Route common configuration](references/route-common.md)
- [Transit route](references/transit-route.md)
- [Walking route](references/walking-route.md)
- [XYZLayer](references/xyz-layer.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated integrations may require a restricted Baidu Maps API key via BMAP_JSAPI_KEY.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
