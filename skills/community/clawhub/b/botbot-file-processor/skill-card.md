## Description: <br>
A file-processing skill for batch renaming files and converting common image, PDF, DOCX, and Markdown formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ollielin](https://clawhub.ai/user/ollielin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to plan and run local batch file renaming and file format conversion tasks. It supports preview-oriented workflows before changing filenames or producing converted files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch renaming can make large sets of filenames difficult to recover if the requested pattern is wrong. <br>
Mitigation: Use dry-run previews, back up important folders, and run the skill only on the intended directory before confirming changes. <br>
Risk: The documentation includes an unused Tencent Cloud/COS dependency note that could cause unnecessary package installation. <br>
Mitigation: Install only the dependencies required for the selected local conversion path unless an independent review confirms the cloud packages are needed. <br>
Risk: Format conversion may fail or produce incomplete outputs when optional tools or libraries are missing. <br>
Mitigation: Confirm required dependencies for the selected conversion type and verify output files after execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ollielin/botbot-file-processor) <br>
- [Poppler Windows releases](https://github.com/oschwartz10612/poppler-windows/releases/) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with Python examples and command-line invocations; scripts create or rename local files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dry-run previews for rename and conversion operations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
