## Description: <br>
Control AirPlay speakers via Airfoil from the command line. Connect, disconnect, set volume, and manage multi-room audio with simple CLI commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asteinberger](https://clawhub.ai/user/asteinberger) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and macOS users use this skill to let an agent manage Airfoil-connected AirPlay speakers, including listing speakers, connecting or disconnecting rooms, setting volume, and checking playback status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted speaker names may be interpreted as unintended AppleScript commands when passed through the shell script. <br>
Mitigation: Use only trusted speaker names, avoid names with quotes or unusual syntax, validate volume values manually, and consider patching the script to pass speaker names as osascript arguments before use. <br>
Risk: The skill requires macOS Accessibility permissions for the terminal or agent environment controlling Airfoil. <br>
Mitigation: Grant Accessibility permissions only to trusted environments and revoke them when the skill is no longer needed. <br>


## Reference(s): <br>
- [Airfoil for Mac](https://rogueamoeba.com/airfoil/mac/) <br>
- [ClawHub Airfoil Skill](https://clawhub.ai/asteinberger/airfoil) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs on macOS with Airfoil, osascript, and macOS Accessibility permissions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
