## Description: <br>
Inspect, validate, summarize, and troubleshoot GeoJSON files and payloads, including FeatureCollection checks, geometry counting, bbox generation, coordinate range review, and CRS-related safety guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvy](https://clawhub.ai/user/jvy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, GIS analysts, and agents use this skill to inspect GeoJSON files or inline payloads, validate common structure issues, summarize geometry content, compute bounding boxes, and explain CRS or coordinate-order uncertainty. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-supplied GeoJSON files or inline payloads for inspection. <br>
Mitigation: Point it only at files or payloads intended for analysis; evidence indicates local read-only behavior with no hidden network transmission. <br>
Risk: GeoJSON coordinate order and CRS assumptions can be wrong for ambiguous or nonstandard data. <br>
Mitigation: Report uncertainty explicitly, confirm the source CRS when precision matters, and recommend reprojection before distance or area analysis. <br>
Risk: The helper validates common structural mistakes but is not a full GIS transformation or editing tool. <br>
Mitigation: Use the skill for inspection and troubleshooting, and hand off to a dedicated GIS tool for conversion, reprojection, clipping, or raster/vector processing. <br>


## Reference(s): <br>
- [GeoJSON Notes](references/geojson-notes.md) <br>
- [ClawHub skill page](https://clawhub.ai/jvy/geojson) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown narrative with optional JSON emitted by the local Python helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include GeoJSON type, feature count, geometry counts, bounding box, coordinate warnings, CRS notes, validation errors, and recommended handoff for GIS processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
