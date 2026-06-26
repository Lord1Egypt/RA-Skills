## Description: <br>
OpenClaw configuration rollback guardian with automatic backup and recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cxlhyx](https://clawhub.ai/user/cxlhyx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor OpenClaw configuration changes, back up known-good configurations, restart the gateway, and roll back changes when message activity does not resume within the configured timeout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Status messages are sent to a hard-coded Matrix room/account. <br>
Mitigation: Remove the message sends or parameterize the room and account before running the guard. <br>
Risk: The guard can restart the gateway and automatically roll back openclaw.json. <br>
Mitigation: Review the script, set paths for the local environment, and enable the systemd service only when persistent automated rollback is desired. <br>
Risk: An incorrect SESSION_FILE can cause successful configuration changes to be treated as failed. <br>
Mitigation: Set SESSION_FILE to the local agent session file before starting the guard. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cxlhyx/continuous-openclaw-config-guard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and operating guidance for a local guard script and optional systemd service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
