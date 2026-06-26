## Description: <br>
Control a Linux X11 desktop by taking screenshots and moving/clicking/typing via xdotool + scrot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rylena](https://clawhub.ai/user/rylena) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to operate Linux X11 GUI workflows by taking screenshots, selecting windows, clicking, typing, and sending key commands in a supervised desktop session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control of a live X11 desktop session, including clicking, typing, key presses, window activation, and URL opening. <br>
Mitigation: Use it only in a dedicated VM, test account, or supervised session, and require explicit approval before actions that could change accounts, send messages, make purchases, or launch external content. <br>
Risk: Screenshots can capture sensitive information from the active desktop. <br>
Mitigation: Close sensitive windows before use and delete generated screenshots when they are no longer needed. <br>
Risk: URL and application launching behavior is under-documented in the release evidence. <br>
Mitigation: Review and constrain open or activate commands to expected targets before allowing an agent to execute them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rylena/claw-mouse) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Configuration] <br>
**Output Format:** [PNG screenshots and terminal text from desktopctl.py commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Linux X11 with python3, xdotool, and scrot; control actions affect the active desktop session.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
