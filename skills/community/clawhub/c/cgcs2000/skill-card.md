## Description: <br>
Explain and work with the CGCS2000 coordinate reference system for China geospatial workflows, including EPSG:4490 interpretation, projected CRS selection, Gauss-Kruger zoning, axis/unit checks, and comparison with WGS84, GCJ-02, and BD-09. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvy](https://clawhub.ai/user/jvy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External GIS users, surveyors, developers, and engineers use this skill to interpret CGCS2000 coordinates, choose between EPSG:4490 and projected CGCS2000 CRS variants, and avoid common China CRS mistakes before conversion or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect CRS assumptions can produce misleading survey, cadastral, engineering, or legal results. <br>
Mitigation: Verify the official CRS, projection zone, coordinate units, axis order, and source coordinate system before relying on recommendations. <br>
Risk: China map-app coordinates may be GCJ-02 or BD-09 rather than raw CGCS2000. <br>
Mitigation: Confirm the acquisition source and offset system before labeling or transforming the coordinates as CGCS2000. <br>


## Reference(s): <br>
- [CGCS2000 Reference](references/cgcs2000-reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/jvy/cgcs2000) <br>
- [Publisher profile](https://clawhub.ai/user/jvy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces CRS interpretation, validation questions, comparison notes, and recommended next steps; it does not execute file-based reprojection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
