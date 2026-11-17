## Description:

Provides guidance for building geospatial OSINT dashboards that combine public location data sources, 3D globe visualization, satellite and aircraft tracking, maritime and seismic layers, and post-processing display modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imjohnathanblog-spec](https://clawhub.ai/user/imjohnathanblog-spec)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to plan and build real-time geospatial intelligence dashboards that aggregate public aviation, maritime, satellite, seismic, mapping, and camera data. It is best suited for implementation guidance, source selection, visualization architecture, and agent-assisted dashboard development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Aggregating public-location intelligence can expose privacy-sensitive patterns, especially when combining aviation, maritime, camera, and regional monitoring data.

Mitigation: Use only lawful and authorized sources, restrict regions and data categories to the approved use case, and add logging and review before storing, sharing, or acting on aggregated observations.

Risk: CCTV aggregation may include exposed private camera feeds or feeds without clear reuse rights.

Mitigation: Do not use camera feeds unless usage rights are clear; require explicit user approval and document the permitted source before adding camera overlays.

Risk: Automated alerts for military or geopolitical activity can amplify misleading or sensitive interpretations.

Mitigation: Keep automated monitoring bounded by source, region, and rate limits, and require human review before alert escalation or publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imjohnathanblog-spec/skills/geospatial-osint)
- [Publisher profile](https://clawhub.ai/user/imjohnathanblog-spec)
- [ADS-B Exchange API Reference](references/adsb-api.md)
- [Cesium.js Basics](references/cesium-basics.md)
- [Post-Processing Effects](references/effects.md)
- [Rendering Stack Deep Dive](references/rendering-stack.md)
- [Satellite Pass Prediction](references/satellite-passes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, shell command examples, API references, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; outputs should be reviewed before implementation against lawful data-source access, privacy, rate-limit, and monitoring constraints.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
