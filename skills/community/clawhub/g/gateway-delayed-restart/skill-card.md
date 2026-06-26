## Description: <br>
Schedules an OpenClaw Gateway restart after a configurable delay and reports completion status, including optional Feishu notification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanl754](https://clawhub.ai/user/hanl754) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators maintaining OpenClaw Gateway use this skill to schedule immediate or delayed gateway restarts during troubleshooting, recovery, or maintenance and to receive a completion report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restart status may be sent to a fixed Feishu recipient that the installer does not control. <br>
Mitigation: Replace the hard-coded Feishu target with a recipient controlled by the installer, or disable notification behavior before running the scripts. <br>
Risk: Running the skill can interrupt OpenClaw Gateway availability. <br>
Mitigation: Run it only during an approved maintenance or recovery window when a gateway restart is acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hanl754/gateway-delayed-restart) <br>
- [OpenClaw Gateway documentation](https://docs.openclaw.ai/gateway) <br>
- [OpenClaw CLI documentation](https://docs.openclaw.ai/cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown prose with shell and Python examples plus terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute OpenClaw gateway restart commands and send Feishu completion notifications when run.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
