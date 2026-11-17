## Description:

批量下载影视/音频资源：夸克网盘直链、BT磁力、B站，含风控评估、断点续传、完整性校验与归档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[czyyr008](https://clawhub.ai/user/czyyr008)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan and execute batch downloads from Quark Drive, BT/magnet links, and Bilibili, with risk assessment, resumable transfers, integrity checks, and media organization. Users should apply it only to content they are authorized to access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill extracts live Quark browser cookies and stores them locally in plaintext.

Mitigation: Store cookies only in a local credentials directory with restrictive file permissions, avoid shared or synced folders, and rotate or delete cookies after use.

Risk: The skill documents provider-limit circumvention and bulk downloading workflows that may trigger account restrictions or misuse.

Mitigation: Use the skill only for content the user is authorized to access, review provider terms and account risk before execution, and keep concurrency within documented limits.

Risk: Download manifests and output paths can cause unintended file writes or overwrites.

Mitigation: Review TSV and magnet manifests before execution, constrain output directories to the intended workspace, and avoid sensitive or shared target paths.

## Reference(s):

- [Batch Downloader Playbook](references/playbook.md)
- [ClawHub Skill Page](https://clawhub.ai/czyyr008/skills/batch-downloader)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with command examples and bundled Python/JavaScript scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces download plans, command invocations, status summaries, manifest guidance, and local file operations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
