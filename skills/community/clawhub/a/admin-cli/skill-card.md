## Description: <br>
Admin Cli helps an agent run privileged administrative commands to update an Arch Linux system, restart systemd services, and report OS status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fabglitch](https://clawhub.ai/user/fabglitch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and system administrators use this skill when they want an agent to help with routine Linux host administration tasks that require elevated privileges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Privileged commands can update packages or restart services on the host. <br>
Mitigation: Require explicit human approval before execution and run the skill only on hosts where these administrative actions are intended. <br>
Risk: The restart-service command can affect arbitrary systemd services if unrestricted. <br>
Mitigation: Limit which services may be restarted through agent or host policy and review the target service before restart. <br>
Risk: The update workflow is specific to Arch pacman and may not be appropriate on other distributions. <br>
Mitigation: Use it only on Arch-based systems or adapt the update command for the target operating system before enabling it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fabglitch/admin-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires elevated privileges for update and service restart workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
