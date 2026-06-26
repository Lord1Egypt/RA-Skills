## Description: <br>
Manages OpenClaw gateway instances by detecting configurations, checking status, scanning ports, changing ports, restarting gateways, creating instances, and deleting instances with confirmation and backup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seastaradmin](https://clawhub.ai/user/seastaradmin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage local and multi-distribution OpenClaw gateway instances, including status checks, port changes, restarts, instance creation, verification, and deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit OpenClaw configuration, scan local ports, restart gateways, and create auto-starting user services. <br>
Mitigation: Install only when those actions are expected, use trusted instance names and numeric ports, and review any created LaunchAgent or user service entries. <br>
Risk: Deleting an instance removes configuration and related local data after confirmation. <br>
Mitigation: Back up important OpenClaw data before use, rely on the documented confirmation prompts, and verify backup directories before removing them. <br>
Risk: Server security evidence reports a suspicious verdict because background service creation uses loosely validated user input. <br>
Mitigation: Use simple trusted instance names, avoid shell metacharacters or untrusted input, and inspect generated service files before loading them. <br>


## Reference(s): <br>
- [OpenClaw Gateway Manager on ClawHub](https://clawhub.ai/seastaradmin/gateway-manager) <br>
- [Common Ports Reference](references/common-ports.md) <br>
- [Security Response](SECURITY_RESPONSE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local paths, ports, process status, and command output for OpenClaw gateway management.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence release and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
