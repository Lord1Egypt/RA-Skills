## Description: <br>
Provides a local OpenClaw Gateway watchdog that restores the newest saved configuration backup and restarts the gateway when the gateway is detected as down. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[segasonicye](https://clawhub.ai/user/segasonicye) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill during local configuration changes to roll back to a saved OpenClaw configuration and restart the gateway after a failed change. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The watchdog can overwrite ~/.openclaw/openclaw.json from the newest backup and force-restart OpenClaw Gateway. <br>
Mitigation: Run it manually only during a confirmed configuration-change window, and inspect the selected backup before allowing rollback. <br>
Risk: The rollback behavior may be broader than the stated 10-second and backup-script-only protection. <br>
Mitigation: Avoid scheduling it as a background watchdog until trigger timing, confirmation, and rollback scope are tightened. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/segasonicye/claw-seatbelt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command and configuration-file behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May replace ~/.openclaw/openclaw.json from the newest backup and force-restart OpenClaw Gateway when invoked.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata; artifact skill.json lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
