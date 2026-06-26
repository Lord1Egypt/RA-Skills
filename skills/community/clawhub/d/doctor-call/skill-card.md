## Description: <br>
Diagnose and fix OpenClaw gateway issues with optional auto-restart via systemd. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stigg86](https://clawhub.ai/user/stigg86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use Doctor Call to diagnose gateway health, run repair commands, restart the gateway when it is down, and enable a user-level systemd timer for recurring health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup command creates opt-in user-level systemd persistence that can repeatedly run repair and restart actions. <br>
Mitigation: Review the setup behavior before enabling it, confirm the timer with systemctl --user, and use doctor-call remove to disable auto-restart. <br>
Risk: The documented auto-restart interval is inconsistent: some text says every hour while the timer behavior is every 5 minutes. <br>
Mitigation: Confirm the desired timer interval before relying on the schedule, and edit or disable the user timer if the cadence is not appropriate. <br>
Risk: The fix path can restart the OpenClaw gateway and run repair commands. <br>
Mitigation: Run check or status first, review the reported state, and use fix or setup only where automatic repair and restart behavior is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stigg86/doctor-call) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and shell-command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or remove user-level systemd service and timer files when setup or remove commands are run.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
