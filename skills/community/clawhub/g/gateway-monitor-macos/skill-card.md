## Description: <br>
Install and operate a local OpenClaw Gateway Monitor stack on macOS with LaunchAgent and watchdog support for setup, repair, validation, one-command install, uninstall, status checks, and automatic launchctl registration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yes999zc](https://clawhub.ai/user/yes999zc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install, run, inspect, repair, and remove a local OpenClaw gateway monitoring service on macOS. It is intended for environments where the user trusts the publisher and accepts a persistent local monitor with administrative gateway actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitor exposes unauthenticated local-admin actions, including gateway restart and OpenClaw config restore. <br>
Mitigation: Run it only on trusted machines, keep access bound to localhost or protected by a firewall, and use restart or restore actions only when you intend to administer the local gateway. <br>
Risk: The persistent LaunchAgent can read OpenClaw logs and status, use local MiniMax credentials, and contact external services. <br>
Mitigation: Review the bundled server and install scripts before installation, confirm credential scope, and uninstall the LaunchAgents when the monitor is no longer needed. <br>
Risk: Gateway repair actions can disrupt active OpenClaw sessions or restore older configuration. <br>
Mitigation: Use the status and backup checks before repair, schedule restarts during maintenance windows, and keep the generated config backups available for recovery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yes999zc/gateway-monitor-macos) <br>
- [Publisher profile](https://clawhub.ai/user/yes999zc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces install, status, uninstall, repair, and validation guidance for a macOS LaunchAgent-based OpenClaw gateway monitor.] <br>

## Skill Version(s): <br>
1.1.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
