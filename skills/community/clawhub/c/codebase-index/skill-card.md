## Description:

代码库索引与理解系统。扫描项目目录，提取所有符号定义（类、函数、变量、导入），构建可搜索的 JSON 索引，支持按名称/类型/文件查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxr-666](https://clawhub.ai/user/lxr-666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan a project, build a searchable JSON symbol index, and query classes, functions, variables, imports, files, and summary statistics while navigating a codebase.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can follow symlinks outside the chosen project.

Mitigation: Avoid running it on untrusted repositories until symlink handling is fixed, and review the scan target before execution.

Risk: Generated JSON indexes may reveal sensitive code metadata such as paths, docstrings, imports, and assigned-value snippets.

Mitigation: Keep generated indexes private and avoid indexing repositories that contain secrets or sensitive implementation details unless sharing controls are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lxr-666/skills/codebase-index)
- [Publisher profile](https://clawhub.ai/user/lxr-666)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands; generated indexes are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated indexes may include file paths, docstrings, imports, symbol names, line numbers, and snippets of assigned values.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
