## Description: <br>
Controls a connected Android device via ADB commands and captures a screenshot after each action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengyang0317](https://clawhub.ai/user/fengyang0317) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and device operators use this skill to translate user requests into ADB actions such as taps, swipes, text input, key events, and device commands, then inspect the resulting screenshot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run broad ADB commands that may install apps, delete data, read files, or change device settings. <br>
Mitigation: Use it only with trusted Android devices, verify the selected target device before execution, and review high-impact commands before running them. <br>
Risk: Screenshots are captured and saved after actions, which can expose sensitive on-device content. <br>
Mitigation: Avoid displaying sensitive content during use and remove saved screenshots when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengyang0317/adb-controller) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Files, Guidance] <br>
**Output Format:** [Plain text command output with a generated PNG screenshot file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Captures and saves a screenshot after each ADB command.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
