## Description:

Explain and work with the CGCS2000 coordinate reference system for China geospatial workflows, including EPSG:4490 interpretation, projected CRS selection, Gauss-Kruger zoning, axis/unit checks, and comparison with WGS84, GCJ-02, and BD-09.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, GIS analysts, surveyors, and mapping practitioners use this skill to interpret CGCS2000 coordinates, choose between EPSG:4490 and projected CGCS2000 CRS variants, compare China coordinate systems, and identify the right next step for validation or reprojection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrectly assuming the source CRS, coordinate order, units, or projected zone can produce misleading CRS guidance or invalid reprojection choices.

Mitigation: Confirm the declared source CRS, coordinate ranges, units, acquisition source, and required projected zone before using guidance for survey, legal, engineering, or production workflows.

Risk: China map-app coordinates may be GCJ-02 or BD-09 rather than raw CGCS2000, and geographic degree coordinates are not suitable for direct measurement.

Mitigation: Verify whether app coordinates use an offset system and choose an exact projected CGCS2000 CRS in meters when measurement, cadastral, engineering, or local analysis is required.

## Reference(s):

- [CGCS2000 Reference](references/cgcs2000-reference.md)
- [ClawHub skill page](https://clawhub.ai/jvy/skills/cgcs2000)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Concise Markdown or plain text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend a QGIS handoff for file-based reprojection, but the skill itself provides CRS interpretation and next-step guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
