## Description: <br>
Command-line interface for VSCode that lets an agent open files, manage workspaces, install or list extensions, and check editor status with optional JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent operators use this skill to control a local VSCode installation from a command line workflow. It is suited for opening project files, adding folders to a workspace, managing extensions, and collecting editor status in text or JSON form. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing untrusted VSCode extensions can change local editor behavior or introduce unwanted code into the development environment. <br>
Mitigation: Approve extension installation deliberately and use trusted extension identifiers. <br>
Risk: Adding folders or opening paths can expose local project context to the editor workflow. <br>
Mitigation: Review folder and file paths before adding them to a workspace or opening them through the skill. <br>
Risk: The Linux setup command uses sudo to create a code command symlink. <br>
Mitigation: Run the sudo setup command only after confirming the target VSCode path is correct. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaising-openclaw1/cli-vscode) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Text, Configuration instructions] <br>
**Output Format:** [Command-line actions with plain text or JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VSCode and the code command-line tool to be installed and available on PATH.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
