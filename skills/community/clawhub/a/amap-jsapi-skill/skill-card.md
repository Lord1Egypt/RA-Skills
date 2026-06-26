## Description: <br>
高德地图 JSAPI v2.0 (WebGL) 开发技能，涵盖地图生命周期管理、强制安全配置、3D 视图控制、覆盖物绘制及 LBS 服务集成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lbs-amap](https://clawhub.ai/user/lbs-amap) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate and verify Gaode Maps JSAPI v2.0 integrations, including map initialization, overlays, view controls, geocoding, routing, search, events, and security configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AMap keys and AMAP_SECURITY_JS_CODE are sensitive credentials that can be exposed if generated code hardcodes them in frontend source or version control. <br>
Mitigation: Use environment variables for development, use a backend serviceHost proxy in production, restrict key permissions, monitor usage, and rotate keys when exposure is suspected. <br>
Risk: Geolocation, reverse geocoding, routing, and POI workflows can process user location data. <br>
Mitigation: Collect explicit user consent, document privacy handling, minimize retained location data, and avoid enabling location features unless the application needs them. <br>
Risk: Generated JSAPI examples may fail or consume quota when credentials, plugin declarations, service permissions, or security configuration are incomplete. <br>
Mitigation: Verify generated code against the bundled references, load only required plugins, check service permissions, and test map loading before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lbs-amap/amap-jsapi-skill) <br>
- [Gaode Maps Developer Homepage](https://lbs.amap.com) <br>
- [Skill Overview](artifact/SKILL.md) <br>
- [Security Configuration](artifact/references/security.md) <br>
- [Map Initialization](artifact/references/map-init.md) <br>
- [Markers](artifact/references/marker.md) <br>
- [Vector Graphics](artifact/references/vector-graphics.md) <br>
- [Geocoder](artifact/references/geocoder.md) <br>
- [Routing](artifact/references/routing.md) <br>
- [Search](artifact/references/search.md) <br>
- [Geolocation API Reference](artifact/references/api/geolocation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript, HTML, CSS, proxy configuration, and framework examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may reference AMAP_JSAPI_KEY and AMAP_SECURITY_JS_CODE and should be checked against the bundled JSAPI references before use.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
