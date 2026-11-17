## Description:

Alibaba Cloud Security Center (SAS) agent onboarding and management assistant for installing and managing Security Center agents, authorization, asset queries, and risk detection through the Aliyun CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud security operators and engineers use this skill to onboard ECS, IDC, and third-party cloud servers to Alibaba Cloud Security Center, manage agent and authorization workflows, and query or trigger security risk detection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect Alibaba Cloud Security Center state, run commands on ECS hosts, install or uninstall endpoint agents, and change paid protection settings.

Mitigation: Use least-privilege temporary credentials or RAM roles and require explicit confirmation before remote install, uninstall, scan dispatch, authorization, or billing-affecting changes.

Risk: Installer and dependency-update patterns can introduce supply-chain or environment-change risk.

Mitigation: Prefer verified Aliyun CLI and agent installation methods and avoid global automatic plugin updates unless reviewed and accepted.

Risk: Incorrect scan command selection can trigger broader account-wide security scans than intended.

Mitigation: Confirm the target scope before scans and reserve full-scan commands for explicit account-wide scan requests.

## Reference(s):

- [Skill Source](artifact/SKILL.md)
- [Agent Install Guide](artifact/references/agent-install-guide.md)
- [Install Scenarios](artifact/references/install-scenarios.md)
- [Management and Query Scenarios](artifact/references/manage-scenarios.md)
- [API Reference](artifact/references/api-reference.md)
- [RAM Permission Manifest](artifact/references/ram-policies.md)
- [CLI Command Reference](artifact/references/related-commands.md)
- [Verification Method](artifact/references/verification-method.md)
- [Acceptance Criteria](artifact/references/acceptance-criteria.md)
- [Alibaba Cloud Security Center Billing Overview](https://help.aliyun.com/zh/security-center/product-overview/billing-overview)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before write operations and avoids exposing credential values.]

## Skill Version(s):

0.0.1 (source: server release evidence, created 2026-06-02T02:38:22Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
