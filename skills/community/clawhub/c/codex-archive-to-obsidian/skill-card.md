## Description:

把 Codex（CLI / 桌面版）的会话记录导出为 Markdown 并归档进 Obsidian 知识库，支持从活动目录与隔离备份双源扫描、噪声剥离、测试会话过滤、自动生成索引。

This skill is ready for commercial/non-commercial use.

## Publisher:

[junci003](https://clawhub.ai/user/junci003)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Codex users use this skill to archive Codex CLI or desktop session history into an Obsidian vault as Markdown notes with a generated index. It is intended for personal knowledge management and session backup workflows where the user controls the vault location.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Archived Codex sessions may contain prompts, code, paths, tool output, or other sensitive conversation content.

Mitigation: Run the dry-run command first, confirm the Obsidian vault path, and avoid syncing or sharing the target vault unless the archived content is appropriate to expose.

Risk: Using the optional reasoning export can preserve additional model reasoning content and increase file size.

Mitigation: Use --with-reasoning only when that extra content is specifically needed; keep the default mode for routine archives.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/junci003/skills/codex-archive-to-obsidian)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files and an Obsidian index, with shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Archives are written under CodexArchive by date; tool output and optional reasoning are truncated by the packaged script.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
