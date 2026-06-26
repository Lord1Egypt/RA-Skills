## Description: <br>
Diagnoses Alibaba Cloud ECS instance reboot or crash issues by checking maintenance events, Cloud Assistant status, system logs, kernel panic or OOM evidence, and Linux or Windows crash dump status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operations engineers and support teams use this skill to investigate unexpected Alibaba Cloud ECS reboots, crashes, kernel panics, OOM events, and missing crash dumps. It guides evidence collection and produces structured diagnostic findings and recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to run remote commands on a target ECS instance through Cloud Assistant. <br>
Mitigation: Use a dedicated least-privilege Alibaba Cloud profile scoped to the intended instance and region, and review each generated command before execution. <br>
Risk: Crash dumps and system logs can contain sensitive operational data. <br>
Mitigation: Limit collection and sharing of logs and dumps to the minimum needed for diagnosis, and confirm disclosure with the user before exposing diagnostic output. <br>
Risk: Some suggested remediation steps may affect instance behavior, such as package installation, bootloader changes, service enablement, or reboot requirements. <br>
Mitigation: Require explicit approval before any package install, bootloader change, service enablement, reboot, or other state-changing action. <br>


## Reference(s): <br>
- [Diagnostic Commands Reference](references/diagnostic-commands.md) <br>
- [Output Format Requirements](references/output-format.md) <br>
- [RAM Permissions](references/ram-policies.md) <br>
- [Common Diagnostic Scenarios](references/scenarios.md) <br>
- [Alibaba Cloud Assistant Installation Guide](https://help.aliyun.com/document_detail/64930.html) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Structured Markdown with inline shell commands, API commands, diagnostic findings, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires instance ID and region ID; diagnostic conclusions are based on collected ECS, Cloud Assistant, system log, and crash dump evidence.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
