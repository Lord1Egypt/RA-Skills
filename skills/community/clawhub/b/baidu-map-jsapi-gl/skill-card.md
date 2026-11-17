## Description:

百度地图 JSAPI WebGL (BMapGL)完整开发指南，覆盖地图初始化、覆盖物、图层、事件、样式、性能优化的任务，一站式开发高性能 3D 地图应用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[baidu-maps](https://clawhub.ai/user/baidu-maps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for Chinese-language guidance and examples when building Baidu Maps JSAPI GL web applications, including map initialization, overlays, layers, events, route planning, local search, geocoding, coordinate conversion, styling, and AK setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Baidu Maps AK that is unrestricted or broadly shared can be misused or exhaust service quota.

Mitigation: Use a browser-side AK with appropriate Referer restrictions, enabled services limited to the application need, and quota monitoring before production use.

Risk: Location, address, route, and POI queries may expose sensitive user or business location data.

Mitigation: Disclose collection, minimize precise location data, avoid unnecessary retention, and handle addresses and coordinates according to the application's privacy requirements.

Risk: Examples that place user-controlled values into HTML strings or use HTTP tile endpoints can introduce content-injection or transport-security issues.

Mitigation: Sanitize or construct DOM content safely and replace HTTP tile URLs with HTTPS endpoints before adopting snippets in production.

## Reference(s):

- [Baidu Maps Open Platform](https://lbsyun.baidu.com/)
- [Baidu Maps API Console](https://lbsyun.baidu.com/apiconsole/key)
- [AK setup](references/get-ak.md)
- [Base classes](references/base-classes.md)
- [Constants](references/constants.md)
- [Map initialization](references/map-init.md)
- [Overlay common operations](references/overlay-common.md)
- [Marker](references/marker.md)
- [Polyline](references/polyline.md)
- [Polygon](references/polygon.md)
- [Circle](references/circle.md)
- [Custom overlay](references/custom-overlay.md)
- [Info window](references/info-window.md)
- [Map events](references/map-events.md)
- [Overlay events](references/overlay-events.md)
- [Map style](references/map-style.md)
- [XYZ layer](references/xyz-layer.md)
- [MVT layer](references/mvt-layer.md)
- [Route common configuration](references/route-common.md)
- [Driving route](references/driving-route.md)
- [Walking route](references/walking-route.md)
- [Riding route](references/riding-route.md)
- [Transit route](references/transit-route.md)
- [Local search](references/local-search.md)
- [Geocoder](references/geocoder.md)
- [Coordinate convertor](references/convertor.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript and HTML code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Baidu Maps browser AK exposed to the agent as BMAP_JSAPI_KEY when examples need authenticated JSAPI access.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter shows 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
