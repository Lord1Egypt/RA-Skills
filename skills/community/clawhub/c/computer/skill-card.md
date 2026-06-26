## Description: <br>
The universal computer skill - hardware diagnostics, system performance, computational tasks, binary operations, and everything about the physical machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlang-cn](https://clawhub.ai/user/openlang-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide computer hardware diagnostics, system health checks, performance monitoring, resource management, optimization, and machine-level troubleshooting across Linux, macOS, and Windows environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad system-administration guidance may lead an agent to propose high-impact changes such as privileged commands, process termination, service restarts, crontab edits, packet capture, remote commands, disk benchmarks, kernel or sysctl tuning, or external reports. <br>
Mitigation: Require explicit user approval before executing those actions, and review the exact command, target host, affected device or service, and rollback plan. <br>
Risk: Performance tuning, disk tests, and hardware diagnostics can disrupt workloads or alter system behavior. <br>
Mitigation: Prefer read-only diagnostics first, avoid production targets for benchmarks and tuning, and confirm backups or maintenance windows before changing kernel, storage, scheduler, or power settings. <br>
Risk: Packet capture, remote commands, and email or Slack reporting can expose sensitive host, network, or operational data. <br>
Mitigation: Limit collection scope, redact secrets and identifiers where practical, and confirm destinations before sending reports or running remote diagnostics. <br>


## Reference(s): <br>
- [Computer on ClawHub](https://clawhub.ai/openlang-cn/computer) <br>
- [openlang-cn publisher profile](https://clawhub.ai/user/openlang-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown skill instructions with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose privileged, destructive, remote, or telemetry-sending system administration commands that require human approval before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
