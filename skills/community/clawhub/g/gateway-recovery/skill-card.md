## Description: <br>
Automatically notifies when the gateway restarts by detecting a recovery flag and sending an "I'm back!" message during heartbeat checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kazuninishiki](https://clawhub.ai/user/kazuninishiki) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure or review an automatic recovery notification flow for a gateway after restart detection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic recovery notifications could be sent to an unintended destination. <br>
Mitigation: Confirm the notification target before installing or enabling the recovery flow. <br>
Risk: A startup hook could run unexpectedly or from an unreviewed local configuration. <br>
Mitigation: Inspect the LaunchAgent or startup hook used on the machine before deployment. <br>
Risk: The recovery flag could be created or modified by an untrusted local user or process. <br>
Mitigation: Ensure the recovery flag path is writable only by trusted local users and processes. <br>


## Reference(s): <br>
- [Gateway Recovery ClawHub page](https://clawhub.ai/kazuninishiki/gateway-recovery) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes a local recovery flag path, startup hook, log path, heartbeat behavior, and manual test steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
