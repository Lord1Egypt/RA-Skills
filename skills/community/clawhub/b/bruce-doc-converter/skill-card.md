## Description: <br>
Converts Word, Excel, PowerPoint, and PDF files to AI-friendly Markdown, and converts Markdown files to Word documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bruc3van](https://clawhub.ai/user/bruc3van) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to convert Office, PDF, and Markdown files, inspect document contents, and export Markdown as Word output when the agent needs file content in a readable format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs an external document conversion CLI in the user's environment. <br>
Mitigation: Prefer pipx or a dedicated virtual environment, and install only in environments where this converter is approved. <br>
Risk: The converter reads document files or directories supplied to the agent. <br>
Mitigation: Run it only on files and folders the user intends the agent to access. <br>
Risk: Failure responses may include a next_command for dependency setup. <br>
Mitigation: Approve only expected setup commands such as bdc setup-node, and reject unexpected commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bruc3van/bruce-doc-converter) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, markdown, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The converter may create Markdown or DOCX files; Office and PDF conversions can include markdown_content for direct analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
