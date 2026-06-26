## Description: <br>
Convert AutoCAD DWG files (1983-2026) to Excel databases using DwgExporter CLI. Extract layers, blocks, attributes, and geometry data without Autodesk licenses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, CAD/BIM engineers, and construction teams use this skill to convert local DWG files into Excel data for layer, block, attribute, geometry, text, quantity-takeoff, and drawing-analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes a local DwgExporter.exe converter, so an untrusted executable could affect local files or produce misleading output. <br>
Mitigation: Install and run only a trusted DwgExporter.exe, and verify the converter path before conversion. <br>
Risk: Recursive or broad batch conversion can process unintended DWG files across a folder tree. <br>
Mitigation: Use explicit input and output paths, and enable recursive batch processing only when the full folder scope is intended. <br>
Risk: Generated Excel and PDF files can contain sensitive CAD project data. <br>
Mitigation: Treat exported XLSX and PDF files as sensitive project artifacts and apply the same access controls as the source DWG files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/dwg-to-excel) <br>
- [cad2data Pipeline](https://github.com/datadrivenconstruction/cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto) <br>
- [DWG to Excel Pipeline video tutorial](https://www.youtube.com/watch?v=jVU7vlMNTO0) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Files] <br>
**Output Format:** [Markdown guidance with CLI and Python code blocks; local XLSX and optional PDF files from DwgExporter.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a locally installed DwgExporter.exe and explicit DWG input paths.] <br>

## Skill Version(s): <br>
2.0.0 (source: claw.json and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
