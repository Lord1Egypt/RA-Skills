## Description:

Alibaba Cloud Lingjun Cluster Manage helps agents manage Alibaba Cloud Lingjun cluster lifecycle tasks, including cluster creation, inspection, deletion, tagging, resource-group changes, and task-status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud Lingjun clusters through guided CLI-backed workflows. It is intended for cluster lifecycle, inventory, tagging, resource-group movement, and task-status interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime and installation paths are not tightly bounded or independently verifiable in the artifact evidence.

Mitigation: Before installing, verify the packaged runtime includes the expected lib/lj_init.sh and review that runtime directly.

Risk: CLI installation guidance includes remote installer paths and an auto-installed eflo-controller plugin.

Mitigation: Prefer signed or package-manager Aliyun CLI installation, avoid curl-to-bash installers, and pin or administratively control the eflo-controller plugin version.

Risk: Cluster lifecycle operations can use broad or long-lived Alibaba Cloud credentials, and DeleteCluster is irreversible.

Mitigation: Use a dedicated low-privilege or short-lived Alibaba Cloud profile, apply scoped RAM policies, tighten DeleteCluster resources to specific clusters in production, and require explicit confirmation for mutating operations.

Risk: The documented internal test-region path requires --insecure, which disables TLS verification.

Mitigation: Do not use the --insecure test-region path with production credentials or production networks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-lingjun-cluster-manage)
- [CLI installation and authentication](references/cli-installation.md)
- [Endpoint routing and region list](references/endpoint-and-regions.md)
- [RAM permission policies](references/ram-policies.md)
- [Async task monitoring](references/async-task-monitoring.md)
- [Error codes reference](references/error-codes.md)
- [Aliyun CLI official docs](https://help.aliyun.com/zh/cli/)
- [Eflo-Controller OpenAPI](https://api.aliyun.com/api/eflo-controller/2022-12-15)
- [Alibaba Cloud Lingjun product page](https://www.alibabacloud.com/product/lingjun)
- [Alibaba Cloud RAM docs](https://www.alibabacloud.com/help/ram)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and text responses with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return markdown tables, confirmation prompts, receipts, and command output summaries.]

## Skill Version(s):

0.0.1-beta.1 (source: server release metadata and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
