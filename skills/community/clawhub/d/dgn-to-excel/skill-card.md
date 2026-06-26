## Description: <br>
Convert DGN files (v7-v8) to Excel databases. Extract elements, levels, and properties from infrastructure CAD files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to convert Bentley MicroStation DGN v7/v8 infrastructure CAD files into Excel workbooks and analyze extracted elements, levels, cells, text, coordinates, and revision changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes an external DgnExporter.exe binary and depends on the executable being trustworthy. <br>
Mitigation: Install the converter only from a trusted source and configure an explicit executable path before running conversions. <br>
Risk: Recursive batch conversion can process broad folder trees and create many Excel outputs, including possible replacement of same-named outputs depending on converter behavior. <br>
Mitigation: Use explicit input folders, review the batch scope before execution, and direct outputs to a controlled working directory. <br>
Risk: The skill needs local filesystem access to read DGN files and write Excel workbooks. <br>
Mitigation: Limit execution to intended project directories and review generated workbooks before sharing them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline command and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local DGN input paths and Excel workbook outputs.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
