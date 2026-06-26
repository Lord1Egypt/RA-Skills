## Description: <br>
Coordinate conversion skill for transforming GeoJSON files and WKT strings across EPSG, CGCS2000, WGS84, GCJ-02, BD-09, geographic, and projected coordinate systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenpipy](https://clawhub.ai/user/chenpipy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, GIS analysts, and engineers use this skill to convert GeoJSON files or WKT geometries between common global and China-specific coordinate systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing pyproj from an untrusted package source could introduce supply-chain risk. <br>
Mitigation: Install pyproj only from a trusted package source before running the conversion script. <br>
Risk: The command can write converted results to a path supplied with --output. <br>
Mitigation: Review the output path before execution and run the tool only on intended GeoJSON or WKT inputs. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, files, guidance] <br>
**Output Format:** [GeoJSON, WKT, or concise Markdown with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print converted results to stdout or write them to a user-specified output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
