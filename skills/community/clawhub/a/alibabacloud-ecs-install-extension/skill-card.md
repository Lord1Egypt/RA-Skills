## Description: <br>
Alibaba Cloud ECS extension installation skill that helps agents query available extensions, check whether a specific extension is available, and install extensions such as OpenClaw, BT Panel, Python environments, and Node.js environments through Alibaba Cloud ECS and OOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud operators, and external users use this skill to list Alibaba Cloud ECS OOS extension packages, verify support for a requested package, and guide installation on one or more ECS instances. It is intended for workflows that require credential checks, RAM permission validation, parameter confirmation, and CLI-based OOS execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change Alibaba Cloud ECS instance state by starting OOS executions and running Cloud Assistant installation workflows. <br>
Mitigation: Require explicit confirmation of region, instance IDs, package name, and installation parameters before execution, and review whether a matching OOS execution is already running. <br>
Risk: The skill requires sensitive cloud credentials and permissions to query and install ECS/OOS extension packages. <br>
Mitigation: Use a least-privilege RAM role or short-lived credentials, avoid entering AccessKeys in chat or shell history, and verify credential status without printing secret values. <br>
Risk: Under-scoped defaults or incorrect CLI parameters can lead to unintended installs or failed operations. <br>
Mitigation: Validate region IDs, ECS instance IDs, package names, and generated JSON parameters before passing them to Alibaba Cloud CLI commands. <br>


## Reference(s): <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [RAM Policies for ECS Extension Installation](references/ram-policies.md) <br>
- [Related Commands](references/related-commands.md) <br>
- [Alibaba Cloud CLI Releases](https://github.com/aliyun/alibaba-cloud-cli/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands, tables, and JSON command parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Alibaba Cloud CLI commands, RAM policy guidance, validation steps, and installation reports.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
