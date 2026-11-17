## Description:

Convert DGN files (v7-v8) to Excel databases. Extract elements, levels, and properties from infrastructure CAD files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Developers and infrastructure CAD engineers use this skill to convert Bentley MicroStation DGN files into Excel workbooks and inspect elements, levels, cells, text, and geometry for reporting and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes a native DGN converter executable.

Mitigation: Use only a trusted absolute path to the converter, verify the executable publisher or hash before use, and run it with limited privileges where possible.

Risk: Batch conversion examples can write Excel outputs across project folders without explicit overwrite safeguards.

Mitigation: Direct batch outputs to a dedicated working folder, review target paths before execution, and keep backups of source project files.

Risk: The skill requests filesystem access for CAD inputs and generated outputs.

Mitigation: Grant access only to the folders needed for the conversion task and avoid running the converter against untrusted DGN files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/skills/dgn-to-excel)
- [cad2data Pipeline](https://github.com/datadrivenconstruction/cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files]

**Output Format:** [Markdown guidance with shell command and Python examples; converted DGN output is an Excel .xlsx workbook when the external converter is run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires filesystem access to read DGN inputs and write Excel outputs.]

## Skill Version(s):

2.0.0 (source: artifact/claw.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
