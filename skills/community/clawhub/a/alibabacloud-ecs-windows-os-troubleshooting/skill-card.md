## Description:

Troubleshoots and helps repair Alibaba Cloud ECS Windows instances from inside the GuestOS or remotely through Cloud Assistant, covering online and offline diagnosis for boot, crash, RDP, network, storage, update, account, certificate, performance, and management-channel issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud operators, and support engineers use this skill to diagnose and plan repairs for Alibaba Cloud ECS Windows instances using local PowerShell or remote Cloud Assistant execution. It is intended for explicit, user-identified ECS Windows targets and includes separate workflows for a running system and a faulty system disk mounted for offline diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote repair workflows can execute Cloud Assistant commands as SYSTEM on a selected ECS Windows instance.

Mitigation: Use the skill only on an explicitly identified instance, verify the target before running commands, and require a fresh user confirmation before any fix.

Risk: Troubleshooting output can include sensitive host, user-data, DNS cache, or configuration details.

Mitigation: Redact sensitive output before sharing logs or diagnostic summaries outside the operating team.

Risk: Some proposed repair actions, optional external tools, or unsigned driver installs can change system state or introduce additional trust concerns.

Mitigation: Review the proposed plan, independently trust any external source, and test risky fixes outside production when practical.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-ecs-windows-os-troubleshooting)
- [Remote Execution Reference Guide](references/REMOTE-EXECUTION.md)
- [Online Workflow Guide](references/online/WORKFLOW-GUIDE.md)
- [Offline Workflow Guide](references/offline/WORKFLOW-GUIDE.md)
- [Platform Evidence Guide](references/online/platform-evidence.md)
- [RAM Policies](references/ram-policies.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with inline PowerShell and Alibaba Cloud CLI command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic summaries, evidence-based conclusions, user-confirmed fix plans, and copyable collection or repair commands.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
