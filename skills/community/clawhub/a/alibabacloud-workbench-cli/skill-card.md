## Description: <br>
Agent-native guidance for using Alibaba Cloud Workbench CLI to manage ECS instances without public IPs, including remote command execution, file transfer, port forwarding, credential setup, instance listing, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud operators, and infrastructure teams use this skill to configure Alibaba Cloud Workbench CLI and operate ECS instances, especially instances without public IP addresses. It supports agent-assisted command execution, file transfer, port forwarding, profile management, and troubleshooting with least-privilege and approval guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables powerful cloud administration actions against Alibaba Cloud ECS instances. <br>
Mitigation: Install and use it only when the agent is intended to administer ECS resources, and scope RAM permissions to specific instances where possible. <br>
Risk: Remote command execution can delete data, interrupt services, or halt systems if used destructively. <br>
Mitigation: Require explicit user approval before destructive commands, including the target instance and expected impact. <br>
Risk: Installer scripts retrieved over the network could be tampered with before execution. <br>
Mitigation: Download and verify the Workbench installer before running it. <br>
Risk: Credential files may contain long-lived Alibaba Cloud access keys. <br>
Mitigation: Prefer temporary role-based credentials when available and keep the Workbench config file restricted with 0600 permissions. <br>
Risk: Automated file uploads can overwrite existing files on remote instances. <br>
Mitigation: Check whether the destination exists and get user confirmation before overwriting remote files. <br>


## Reference(s): <br>
- [Required RAM Permissions](references/ram-policies.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-workbench-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell, PowerShell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Workbench CLI command examples, configuration snippets, RAM policy JSON, output schemas, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
0.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
