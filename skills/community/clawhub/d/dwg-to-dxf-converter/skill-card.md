## Description: <br>
Converts AutoCAD DWG drawings to DXF format on Windows by invoking a local ODA File Converter installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lialia691691-alt](https://clawhub.ai/user/lialia691691-alt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert DWG files or folders into DXF files before downstream CAD parsing or processing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill executes a local converter binary and writes converted files to a user-selected output directory. <br>
Mitigation: Confirm the input and output paths before running, and verify ODAFileConverter.exe comes from a trusted ODA installation or bundled path. <br>


## Reference(s): <br>
- [ODA File Converter](https://www.opendesign.com/guestfiles/oda_file_converter) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Guidance] <br>
**Output Format:** [Markdown guidance with command examples and generated DXF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Windows and a trusted local ODAFileConverter.exe path.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
