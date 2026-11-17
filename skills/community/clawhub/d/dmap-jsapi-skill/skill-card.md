## Description:

DMap GL JSAPI (dmapgl) developer guidance for writing, reviewing, and debugging map initialization, overlays, layers, events, controls, and related map API code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haohaizi0620](https://clawhub.ai/user/haohaizi0620)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as DMap GL JSAPI reference material when implementing or reviewing map components, markers, popups, data sources, layers, controls, events, view control, animation, and terrain features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags insecure HTTP script loading and private endpoint examples.

Mitigation: Use trusted HTTPS origins and pin or vendor DMap scripts before production use.

Risk: The security evidence flags unsafe copy-paste patterns around HTML content.

Mitigation: Avoid setHTML with untrusted data; prefer setText, sanitized DOM construction, or reviewed templates.

Risk: The security evidence flags precise location tracking as a consent-sensitive behavior.

Mitigation: Gate geolocation features behind explicit user consent and disable them unless the use case requires location tracking.

## Reference(s):

- [DMap GL JSAPI Developer Guide](SKILL.md)
- [Map Initialization and Lifecycle](references/map-init.md)
- [View Control](references/view-control.md)
- [Markers](references/marker.md)
- [Popups](references/popup.md)
- [Sources](references/sources.md)
- [Layers](references/layers.md)
- [Controls](references/controls.md)
- [Events](references/events.md)
- [Animation](references/animation.md)
- [Terrain](references/terrain.md)
- [Map API](references/api/map.md)
- [Properties and Options API](references/api/properties.md)
- [Markers and Controls API](references/api/markers-controls.md)
- [Sources API](references/api/sources.md)
- [Events API](references/api/events.md)
- [Geography and Geometry API](references/api/geography.md)
- [Style Specification: Root](references/style/root.md)
- [Style Specification: Layers](references/style/layers.md)
- [Style Specification: Sources](references/style/sources.md)
- [Style Specification: Expressions](references/style/expressions.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript, HTML, and configuration code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill is reference-driven and should be reviewed before copying examples into production.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
