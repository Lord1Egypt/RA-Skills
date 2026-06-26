## Description: <br>
Gateway Guardian monitors the OpenClaw gateway health endpoint, restarts the gateway when it is unavailable, and logs recovery activity on macOS and Linux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators running OpenClaw use this skill to keep a local gateway process available by checking its health endpoint, restarting it, and restoring a backup configuration if needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The watchdog can message a fixed Telegram recipient when gateway recovery fails. <br>
Mitigation: Review guardian.sh before use, remove the hardcoded recipient, and require users to configure alerts explicitly. <br>
Risk: The watchdog can overwrite the local OpenClaw configuration with a backup file during recovery. <br>
Mitigation: Keep an independent backup of ~/.openclaw/openclaw.json and review the configured backup path before enabling automatic restoration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dagangtj/gateway-guardian) <br>
- [Publisher profile](https://clawhub.ai/user/dagangtj) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for running and configuring a Bash watchdog script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
