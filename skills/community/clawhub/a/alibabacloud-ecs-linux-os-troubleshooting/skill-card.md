## Description:

Troubleshoot an Alibaba Cloud ECS Linux OS when a user needs to diagnose a specified ECS Linux instance, such as instance stuck in Starting, boot stuck, SSH/VNC/Workbench login failure, network issues, disk/FS issues, performance anomalies, suspected mining or hidden processes, crash/hang, clock drift, or configuration not taking effect.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support engineers, and cloud operators use this skill to diagnose Alibaba Cloud ECS Linux GuestOS incidents through a structured six-phase workflow. It helps classify the symptom, collect Alibaba Cloud ECS evidence, run approved diagnostic checks, and produce an evidence-backed diagnosis report with next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide powerful Alibaba Cloud ECS diagnostic and recovery workflows on live Linux instances.

Mitigation: Use it only on instances the operator administers, grant least-privilege RAM permissions for the selected workflow, and review RunCommand, diagnostic report, disk, GRUB, sysctl, cache, key-pair, and password operations before allowing them.

Risk: Incorrect region, instance, disk, ENI, or JSON input could target the wrong resource or change command meaning.

Mitigation: Validate identifiers, time windows, and JSON parameters before command execution; stop and ask for corrected values when validation fails.

Risk: Troubleshooting output may include sensitive operational data from cloud commands or the guest operating system.

Mitigation: Exclude secrets, passwords, access keys, and full sensitive command outputs from the final diagnosis report.

## Reference(s):

- [Customer symptom to phenomenon domain routing](references/symptom-to-domain.md)
- [Linux phenomenon domain index](references/phenomenon-domain.md)
- [aliyun CLI Quick Reference](references/aliyun-cli-cheatsheet.md)
- [RAM Policies](references/ram-policies.md)
- [Resource Diagnostic Report Usage Guide](references/create-diagnostic-report.md)
- [Degraded Mode](references/degraded-mode.md)
- [ECS Linux Diagnosis Report](references/diagnosis-report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown diagnosis report with inline shell commands and structured recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes target instance, region, phenomenon domain, issue boundary, key evidence, conclusion confidence, and recommended next actions; excludes secrets and full sensitive command outputs.]

## Skill Version(s):

0.0.1 (source: server release metadata; artifact metadata.version is 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
