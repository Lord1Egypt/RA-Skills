## Description: <br>
Comprehensive Alibaba Cloud ECS instance diagnostics skill that performs systematic troubleshooting across cloud platform status checks and optional guest OS diagnostics via Cloud Assistant. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and cloud operators use this skill to diagnose Alibaba Cloud ECS connectivity, performance, disk, status, and system-event issues by combining read-only platform checks with optional Cloud Assistant guest OS diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill combines diagnostics with high-impact remediation paths and remote command execution on ECS instances. <br>
Mitigation: Start with the read-only RAM policy, use a dedicated least-privilege role, keep Cloud Assistant execution disabled unless needed, and require explicit review before firewall, EIP, instance lifecycle, password, reboot, or guest OS commands. <br>
Risk: Diagnostic access can expose sensitive cloud environment details if commands or reports are handled carelessly. <br>
Mitigation: Review commands before execution, never print access keys or secrets, and keep sensitive values out of diagnostic reports. <br>


## Reference(s): <br>
- [Related Commands](references/related-commands.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Remote Connection Diagnose Design](references/remote-connection-diagnose-design.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown diagnostic report with inline shell commands and remediation recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires confirmed Alibaba Cloud region and ECS instance identifiers; deep diagnostics require explicit user approval.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
