## Description:

ArcGIS Agent lets an AI assistant drive ArcGIS Pro arcpy geoprocessing tools through a localhost HTTP API for GIS automation and spatial analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaojj662](https://clawhub.ai/user/zhaojj662)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, GIS analysts, and agent users use this skill to translate natural-language GIS requests into ArcGIS Pro automation steps, local HTTP calls, and arcpy tool invocations. It is intended for Windows environments with ArcGIS Pro 3.x and a valid ArcGIS license.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes a powerful unauthenticated local ArcGIS automation service that can modify GIS files.

Mitigation: Keep the service bound to localhost, restrict exposed modules with INCLUDE_MODULES, add authentication or keep the port inaccessible to browsers and untrusted local processes, and confirm write operations before execution.

Risk: The automation service can use active ArcGIS Portal or ArcGIS Online authority.

Mitigation: Avoid running it while signed into sensitive Portal or ArcGIS Online accounts unless that access is required and approved.

Risk: Overwrite behavior or broad path access can affect local GIS datasets.

Mitigation: Disable overwriteOutput by default where practical and keep ARCPY_ALLOWED_PATHS limited to intended project directories.

## Reference(s):

- [ArcGIS Agent ClawHub page](https://clawhub.ai/zhaojj662/skills/arcgis-agent)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON request examples, and ArcGIS tool names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local HTTP calls to an ArcGIS automation server and guidance for selecting arcpy modules and tool arguments.]

## Skill Version(s):

1.2.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
