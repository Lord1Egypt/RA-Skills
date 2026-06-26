## Description: <br>
Claw Windows Automator helps an agent drive Windows desktop automation by opening CMD in a selected directory, executing commands or batch scripts, downloading latest GitHub source archives, and showing an interruptible full-screen progress overlay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangminrui2022](https://clawhub.ai/user/wangminrui2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill when an agent needs to run Windows CMD commands, launch batch scripts in a target folder, or download a latest GitHub source archive while displaying visible progress and a manual stop mechanism. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute arbitrary user-provided commands in Windows CMD. <br>
Mitigation: Review every command and working directory before invocation, and run only commands from trusted sources. <br>
Risk: First use may create a reusable virtual environment, change Python packaging tools, and install dependencies. <br>
Mitigation: Inspect dependency changes before execution and use an isolated account, workspace, or disposable environment when testing. <br>
Risk: The GitHub download workflow opens a browser and downloads code from a supplied repository URL. <br>
Mitigation: Use only trusted repository URLs and verify downloaded archives before running their contents. <br>
Risk: GUI automation can send keyboard and mouse input to the active Windows desktop. <br>
Mitigation: Keep the desktop undisturbed while the workflow runs and use the documented left-click stop control if behavior is unexpected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangminrui2022/claw-windows-automator) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Windows automation side effects; requires Python and a Windows desktop session for the documented workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
