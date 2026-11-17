## Description:

Converts GeoJSON files and WKT geometries between WGS84, CGCS2000, Web Mercator, Beijing 1954, GCJ-02, BD-09, and related EPSG coordinate systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenpipy](https://clawhub.ai/user/chenpipy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, GIS analysts, and agents use this skill to prepare coordinate-conversion commands and convert GeoJSON or WKT data between common global and China-specific coordinate systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted geospatial input files may be read and transformed by the local conversion script.

Mitigation: Use trusted GeoJSON or WKT inputs and inspect input paths before running conversion commands.

Risk: A user-selected output path can cause converted results to be written to disk.

Mitigation: Choose output paths deliberately and avoid overwriting important files.

Risk: The documented dependency installation uses an apt package install command.

Mitigation: Review package installation commands in the target environment before executing them.

## Reference(s):

- [Coord Transform ClawHub release page](https://clawhub.ai/chenpipy/skills/coord-transform)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; converted GeoJSON or WKT when the bundled script is run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write converted output to a user-selected file path when an output argument is provided.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
