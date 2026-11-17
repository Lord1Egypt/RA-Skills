## Description:

安全扫描并分析 Windows C 盘空间和文件，支持临时文件清理、重复文件去重及大文件迁移，所有删除或迁移操作都需要用户确认。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zx0018](https://clawhub.ai/user/zx0018)

### License/Terms of Use:

MIT-0

## Use Case:

Windows users and support engineers use this skill to inspect C drive storage usage, identify temporary files, duplicate files, and large files, and prepare cleanup or migration actions. Destructive actions are intended to be performed only after explicit user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WinRM credentials are required for remote Windows access, and sample configuration includes certificate validation set to ignore.

Mitigation: Use a least-privileged WinRM account, store secrets in environment variables or a secrets manager, and configure certificate validation with a trusted certificate before use.

Risk: Cleanup and deduplication actions can delete files from the Windows host.

Mitigation: Run scan-only mode first, review the reported targets, keep protected path rules enabled, and require explicit approval for each delete or cleanup step.

Risk: Migration transfers files from the Windows host to the agent server, which is a data export.

Mitigation: Use migration only when the destination is approved and trusted, confirm the target path before transfer, and avoid configuring migration when files should remain on the Windows host.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zx0018/skills/c-cleaner-zx)
- [README](artifact/README.md)
- [Path assumptions](artifact/references/path-assumptions.md)
- [Safety rules](artifact/references/safety-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, confirmation prompts, command suggestions, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce scan reports, cleanup plans, migration plans, and operation-log guidance; deletion and migration require explicit confirmation.]

## Skill Version(s):

1.0.5 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
