## Description:

Alibaba Cloud ECS File Backup Essential Edition helps agents guide users through activation, backup-plan management, status checks, quota viewing, and file restore operations for Alibaba Cloud Cloud Backup ECS file backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to decide whether Alibaba Cloud ECS File Backup Essential Edition fits an ECS file-backup scenario and to perform supported operations through Aliyun CLI guidance. It covers activation, pause and resume, cancellation, backup status checks, quota viewing, schedule and priority updates, and file restores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that the skill directs broad cloud privileges and unsafe persistent CLI or plugin installation changes.

Mitigation: Review installation steps before use, avoid curl-to-bash installation paths, do not enable persistent automatic plugin installation unless intended, and prefer the documented least-privilege RAM policy over full Cloud Backup access.

Risk: The artifact includes operations that can delete backup plans or overwrite files during restore.

Mitigation: Require explicit user confirmation before destructive delete or overwrite actions and verify target parameters before running generated Aliyun CLI commands.

## Reference(s):

- [CLI Installation Guide](artifact/references/cli-installation-guide.md)
- [RAM Permission Policies](artifact/references/ram-policies.md)
- [Related APIs](artifact/references/related-apis.md)
- [Verification Methods](artifact/references/verification-method.md)
- [ECS File Backup Essential Edition User Guide](https://help.aliyun.com/zh/cloud-backup/user-guide/ecs-file-backup-essential-edition)
- [Cloud Backup API Reference](https://help.aliyun.com/zh/cloud-backup/developer-reference/api-hbr-2017-09-08-overview)
- [Cloud Backup RAM Permission Reference](https://help.aliyun.com/zh/cloud-backup/developer-reference/authorization-rules)
- [Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-cloudbackup-ecs-file-backup-essential-edition)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and CLI parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes eligibility checks, user confirmation gates, command pre-checks, restore verification steps, and credential-handling guidance.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
