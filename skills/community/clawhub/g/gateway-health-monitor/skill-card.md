## Description: <br>
Monitors and helps troubleshoot OpenClaw gateway stability issues on macOS, including launchd throttling, plugin restart loops, hung shutdowns, and power-management interference. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimmyclanker](https://clawhub.ai/user/jimmyclanker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who run OpenClaw gateways on macOS use this skill to diagnose downtime, restart loops, launchd throttling, hung shutdowns, and power-management interference, then apply documented remediation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional patcher installer creates a persistent launchd agent that watches and modifies the OpenClaw gateway plist. <br>
Mitigation: Review the patcher scripts before running them, install only on intended macOS OpenClaw gateway hosts, and keep a rollback plan for unloading the patcher and restoring plist defaults. <br>
Risk: The documented Power Nap command changes a machine-wide macOS power-management setting. <br>
Mitigation: Run the command only when you accept the host-wide behavior change and have appropriate administrative approval. <br>
Risk: Remediation commands can alter launchd service behavior and gateway restart policy. <br>
Mitigation: Review diagnostic output first, back up relevant plist and OpenClaw configuration files, and apply changes deliberately rather than as unattended commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jimmyclanker/gateway-health-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and optional shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes diagnostic checks and remediation guidance for macOS launchd, OpenClaw gateway configuration, plist settings, and power-management settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
