## Description: <br>
Helps an agent use pymavlink to connect to and control ArduPilot drones, including status checks, arming, takeoff, movement, and landing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LuweiLiao](https://clawhub.ai/user/LuweiLiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and drone operators use this skill to draft pymavlink-based procedures and code snippets for ArduPilot status checks, guided takeoff, relative movement, and landing. It should be tested in simulation and reviewed by a qualified human before any real drone operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward commands that force-arm, launch, move, or land a real ArduPilot drone without built-in safety boundaries. <br>
Mitigation: Test in simulation first, require explicit human approval before arming or takeoff, supervise all operation, and add preflight, geofence, battery, GPS, and emergency-stop procedures before connecting to real hardware. <br>
Risk: Unverified dependencies or environment setup could affect drone-control behavior. <br>
Mitigation: Pin and verify pymavlink before use and review generated commands and code before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LuweiLiao/ardupilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides operational examples for pymavlink connection, status checks, arming, takeoff, movement, landing, and dependency installation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
