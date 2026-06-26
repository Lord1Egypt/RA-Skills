## Description: <br>
Open-source geospatial intelligence gathering and visualization guidance for building Worldview-style dashboards that combine satellite tracking, flight and maritime data, street cameras, seismic feeds, and real-time 3D visualization effects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imjohnathanblog-spec](https://clawhub.ai/user/imjohnathanblog-spec) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OSINT analysts use this skill to design browser-based geospatial dashboards that integrate public aviation, maritime, satellite, seismic, camera, and map data with Cesium.js-style visualization workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive OSINT workflows can enable privacy-invasive or unlawful monitoring when applied to individuals, private spaces, or restricted data sources. <br>
Mitigation: Use lawful public sources, follow API and camera-site terms, avoid monitoring individuals or private spaces, and add explicit privacy and responsible-use safeguards before deployment. <br>
Risk: Example integrations use API keys and public data services that may expose credentials or exceed third-party terms if copied directly into a client-side dashboard. <br>
Mitigation: Keep API keys out of client-side code where possible, use server-side secret handling or proxying, and review each provider's access and rate-limit terms before use. <br>
Risk: Live public feeds can be incomplete, delayed, mislabeled, or misleading when combined into operational geospatial views. <br>
Mitigation: Display source attribution and timestamps, cross-check important observations against multiple sources, and require human review before acting on alerts. <br>


## Reference(s): <br>
- [Cesium.js Basics](references/cesium-basics.md) <br>
- [Rendering Stack Deep Dive](references/rendering-stack.md) <br>
- [ADS-B Exchange API Reference](references/adsb-api.md) <br>
- [Satellite Pass Prediction](references/satellite-passes.md) <br>
- [Post-Processing Effects](references/effects.md) <br>
- [Geospatial Osint ClawHub Release](https://clawhub.ai/imjohnathanblog-spec/geospatial-osint) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and reference links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes dashboard architecture, data-source notes, example integrations, visualization effects, and responsible-use guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
