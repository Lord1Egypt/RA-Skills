## Description:

自动文件归档与整理技能，用于在创建、下载、复制、接收或整理工作空间文件时，将新增文件按类型归入 user/ 目录，同时避免改动 OpenClaw 原生文件和已结构化项目目录。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyh-longying](https://clawhub.ai/user/xyh-longying)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace users use this skill to keep OpenClaw workspaces tidy by placing newly created, generated, downloaded, copied, or received files under categorized user/ subdirectories. It is intended for loose workspace files, not for moving native OpenClaw files or already structured project directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reorganizing existing loose workspace files may break user workflows that depend on current paths.

Mitigation: Ask for user confirmation before moving existing files, especially in workspaces where file paths matter.

Risk: File organization could accidentally affect protected OpenClaw files or already structured project directories.

Mitigation: Keep OpenClaw native files and folders unchanged, and do not move structured project directories.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xyh-longying/skills/f-org)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with path conventions, file-category rules, and examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code, network access, credential handling, or persistence is disclosed by the security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
