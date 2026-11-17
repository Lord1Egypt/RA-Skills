## Description:

Inspect, validate, summarize, and troubleshoot GeoJSON files and payloads, including FeatureCollection checks, geometry counting, bbox generation, coordinate range review, and CRS-related safety guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and GIS practitioners use this skill to inspect GeoJSON files or inline payloads, summarize geometry content, compute bounding boxes, and identify common coordinate or structure problems before deeper GIS work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user-provided file path may point to sensitive local data.

Mitigation: Review the path before inspection and only provide GeoJSON files intended for analysis.

Risk: Coordinate order or CRS assumptions can lead to misleading spatial interpretation.

Mitigation: Confirm the source CRS and coordinate order when precision matters, and use a dedicated GIS tool for reprojection, measurement, clipping, conversion, or editing.

## Reference(s):

- [GeoJSON Notes](references/geojson-notes.md)
- [ClawHub GeoJSON Release](https://clawhub.ai/jvy/skills/geojson)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include validation errors, geometry counts, bounding boxes, coordinate-range notes, and CRS guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
