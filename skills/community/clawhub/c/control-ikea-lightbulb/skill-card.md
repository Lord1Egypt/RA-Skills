## Description: <br>
Control IKEA/TP-Link Kasa smart bulbs on a local LAN by IP, including on/off state, brightness, and color. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antgly](https://clawhub.ai/user/antgly) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and home automation users can use this skill to operate a local Kasa-compatible smart bulb by IP address without cloud credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands control a local smart bulb at a user-specified IP address. <br>
Mitigation: Verify the target IP address and run commands only against the intended LAN device. <br>
Risk: Light-show and flashing modes may be disruptive or unsafe in some environments. <br>
Mitigation: Use flashing modes cautiously and avoid them where rapid light changes may be inappropriate. <br>
Risk: The skill depends on uv and the python-kasa package source used at install time. <br>
Mitigation: Install dependencies from trusted package sources before running the scripts. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Controls a user-specified local Kasa-compatible bulb over the LAN.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
