## Description: <br>
Controls Windows desktop applications by launching, focusing, resizing, moving, and closing windows, simulating keyboard and mouse input, managing processes, controlling VS Code, reading clipboard data, and capturing screen information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lexylent](https://clawhub.ai/user/Lexylent) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and power users use this skill to let an agent automate Windows desktop workflows, inspect active windows, send keyboard or mouse input, manage processes, and interact with VS Code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad desktop automation can affect open applications, active windows, and user data. <br>
Mitigation: Use only on a Windows desktop where agent control is intended, focus the target window before input, and require explicit confirmation before app launches, closing windows, process killing, typing, clicking, and VS Code extension changes. <br>
Risk: Screenshots and clipboard reads may expose sensitive information. <br>
Mitigation: Keep secrets off-screen and out of the clipboard before use, and require explicit confirmation before screenshots, clipboard reads, or clipboard writes. <br>
Risk: The PowerShell scripts are published as text files and must be renamed before use. <br>
Mitigation: Review the scripts before renaming or running them, then run only the specific command needed for the user-approved task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lexylent/desktop-control-win) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline PowerShell command examples and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing desktop automation guidance and PowerShell command invocations; scripts may create screenshots or read clipboard text when explicitly run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
