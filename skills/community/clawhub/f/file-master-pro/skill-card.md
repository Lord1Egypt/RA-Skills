## Description:

强大的文件批量处理工具，支持重命名、整理、搜索、转换等操作，让文件管理变得简单高效。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shengjun33333-code](https://clawhub.ai/user/shengjun33333-code)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage local files through command-line workflows for batch renaming, type-based organization, content search, and duplicate detection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local rename and organize operations can modify or move many files recursively.

Mitigation: Review the target directory, keep an external backup, and test on non-critical folders before running broad operations.

Risk: The installer creates files under the user profile and may attempt to add a command shim or symlink to the system PATH.

Mitigation: Review install.py before installation, avoid elevated privileges, and check for an existing file-master command before installing.

Risk: The documentation advertises delete, convert, compress, undo, and automation behavior that is unsupported in this artifact.

Mitigation: Rely only on the implemented commands: rename, organize, search, and find-duplicates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shengjun33333-code/skills/file-master-pro)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [File Master documentation](https://docs.file-master.pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact includes a local Python CLI that returns JSON for implemented file operations.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
