## Description:

Convert AutoCAD DWG files (1983-2026) to Excel databases using DwgExporter CLI. Extract layers, blocks, attributes, and geometry data without Autodesk licenses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Developers, CAD/BIM engineers, and construction data teams use this skill to convert local DWG drawings into Excel datasets and help analyze layers, blocks, attributes, geometry, text, and drawing summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Excel or PDF outputs can expose sensitive project annotations, attributes, coordinates, layouts, and other drawing metadata.

Mitigation: Treat converted outputs as sensitive project files and share or store them under the same access controls as the source DWG.

Risk: The skill executes a local DWG conversion tool against user-selected files.

Mitigation: Use only trusted local DWG paths and a verified DwgExporter installation when running conversion commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/skills/dwg-to-excel)
- [cad2data pipeline repository](https://github.com/datadrivenconstruction/cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto)
- [DWG to Excel pipeline video tutorial](https://www.youtube.com/watch?v=jVU7vlMNTO0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local file conversion and analysis; generated Excel and PDF outputs are created by the local DwgExporter CLI.]

## Skill Version(s):

2.0.0 (source: artifact/claw.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
