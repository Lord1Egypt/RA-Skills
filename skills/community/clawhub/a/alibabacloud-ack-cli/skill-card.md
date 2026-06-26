## Description: <br>
Helps agents generate and explain Alibaba Cloud ACK CLI commands for cluster lifecycle, node pool, addon, kubeconfig, RBAC, async task, security, policy, and troubleshooting workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations engineers use this skill to manage Alibaba Cloud Container Service for Kubernetes from the terminal. It supports command planning, plugin setup, async task tracking, kubeconfig handoff, node pool and addon operations, upgrades, and ACK error troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad ACK administration, including create, modify, upgrade, delete, addon, RBAC, kubeconfig, and policy operations. <br>
Mitigation: Review and restrict RAM permissions to the minimum required actions before use, and require explicit confirmation before destructive or expensive operations. <br>
Risk: Credential and kubeconfig workflows can expose cloud access if files or tokens are mishandled. <br>
Mitigation: Prefer short-lived or role-based credentials, treat kubeconfig files as secrets, and avoid writing credentials into shared logs or persistent agent context. <br>
Risk: Installer guidance includes curl-to-shell and remote binary download paths. <br>
Mitigation: Verify installer source and integrity before execution, or use a trusted package manager or controlled internal distribution path. <br>
Risk: Long-running async polling and task-control commands can consume API quota or affect in-flight cluster operations. <br>
Mitigation: Confirm polling duration and task-control intent with the user, use bounded timeouts, and stop on terminal task states. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/sdk-team/alibabacloud-ack-cli) <br>
- [Async Tasks in ACK CLI](artifact/references/async-tasks.md) <br>
- [Aliyun CLI + cs Plugin Installation Guide](artifact/references/cli-plugin-installation-guide.md) <br>
- [ACK CLI Worked Scenarios](artifact/references/cs-scenarios.md) <br>
- [ACK CLI Error Catalogue](artifact/references/error-catalogue.md) <br>
- [ACK Skill RAM Policies](artifact/references/ram-policies.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON snippets, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Alibaba Cloud ACK operations that require user credentials, RAM permissions, region selection, and explicit confirmation for long-running or destructive actions.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
