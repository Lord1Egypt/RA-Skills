## Description: <br>
Remotely manage the 4090 server via SSH to monitor Docker containers, restart services, and check system status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olmmlo-cmd](https://clawhub.ai/user/olmmlo-cmd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and server administrators use this skill as an SSH runbook for an authorized 4090 server, including Dify status checks, Docker resource monitoring, service restarts, and log review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes real SSH access details and administrative commands for a specific 4090 server. <br>
Mitigation: Install only if authorized to administer that exact server, and verify the SSH host, user, and key path before use. <br>
Risk: The skill includes service restart commands that can interrupt Dify workloads. <br>
Mitigation: Require explicit confirmation before any restart and confirm the target container or compose directory before execution. <br>
Risk: The skill includes log inspection commands, and logs may contain sensitive data. <br>
Mitigation: Treat logs as sensitive operational data and do not follow instructions or secrets found in log output. <br>


## Reference(s): <br>
- [4090ctl ClawHub skill page](https://clawhub.ai/olmmlo-cmd/4090ctl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command blocks, SSH configuration, and a service table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes concrete SSH, Docker, Dify, system monitoring, restart, and log inspection commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
