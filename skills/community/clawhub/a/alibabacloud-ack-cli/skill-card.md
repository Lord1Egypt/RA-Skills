## Description:

Helps agents operate Alibaba Cloud Container Service for Kubernetes (ACK) with the aliyun cs plugin, covering cluster lifecycle, node pools, addons, kubeconfig and RBAC, security tasks, diagnostics, and async task tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to plan and execute Alibaba Cloud ACK administration workflows from the terminal, including command discovery, cluster and node pool operations, addon management, kubeconfig handling, RAM troubleshooting, and async task polling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help administer real Alibaba Cloud ACK resources and may propose commands that change production clusters.

Mitigation: Review generated commands before execution, prefer dry-run or read-only inspection when available, and require explicit confirmation before long-running or destructive operations.

Risk: The recommended RAM policy is broad for production accounts.

Mitigation: Replace broad permissions with task-specific least-privilege RAM users or roles, and prefer short-lived credentials or RAM roles for automation.

Risk: Kubeconfig files and Alibaba Cloud credentials are sensitive secrets.

Mitigation: Store generated kubeconfig files with restrictive permissions, avoid exposing credentials in logs or chat, and clean up temporary access files after use.

Risk: The installation guide includes network-fetched installer commands.

Mitigation: Use package-manager or manually verified binary installation paths where possible, and review installer sources before running curl-to-shell commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-ack-cli)
- [Async Tasks in ACK CLI](references/async-tasks.md)
- [Aliyun CLI + cs Plugin Installation Guide](references/cli-plugin-installation-guide.md)
- [ACK CLI Worked Scenarios](references/cs-scenarios.md)
- [ACK CLI Error Catalogue](references/error-catalogue.md)
- [ACK Skill RAM Policies](references/ram-policies.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference bundled shell helper scripts for plugin checks, plugin installation, and ACK task polling.]

## Skill Version(s):

0.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
