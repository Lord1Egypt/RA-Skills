## Description:

Helps manage Alibaba Cloud Lingjun cluster expansion and shrinking, node groups, and moving nodes between groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Infrastructure operators and developers use this skill to plan and request Lingjun cluster scaling and node-group changes, and to check operation status through Alibaba Cloud.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cluster changes can modify or purchase Alibaba Cloud infrastructure.

Mitigation: Grant only the necessary RAM permissions and review proposed changes before confirming.

Risk: Credentials, node login passwords, or operation details may be exposed through weak local secret and state handling.

Mitigation: Prefer temporary credentials, avoid reusable node login passwords, and restrict access to local operation data.

Risk: Key runtime files are missing from this package, making operational workflows unreliable.

Mitigation: Request publisher fixes and verify a complete package before production use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-lingjun-cluster-scaling)
- [Aliyun CLI installation guide](artifact/references/cli-installation-guide.md)
- [Alibaba Cloud CLI documentation](https://help.aliyun.com/zh/cli/)
- [Lingjun API documentation](https://help.aliyun.com/zh/pai/developer-reference/api-eflo-controller-2022-12-15-overview)
- [Supported regions](artifact/references/supported-regions.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Forms, confirmation receipts, and task-status responses for supported operations.]

## Skill Version(s):

0.0.1-beta.3 (source: ClawHub release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
