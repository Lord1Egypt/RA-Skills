## Description:

Manages long-term project context and session-resume checkpoints for git and non-git projects, including project adoption, drift checks, checkpointing, and recovery from file-based state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[holdyounger](https://clawhub.ai/user/holdyounger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project maintainers use this skill to keep long-running project state recoverable across sessions, especially when resuming work, saving checkpoints, adopting existing directories, or tracking uncheckpointed git and file changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initialization can persistently modify repositories and workspace files, including .ctx-lockstep content and workspace-level project rules.

Mitigation: Use it only on intended project paths, confirm exact target paths before initialization, and avoid overwrite mode unless the existing files have been reviewed.

Risk: The skill can add a persistent post-commit hook to git repositories.

Mitigation: Inspect any existing .git/hooks/post-commit before initialization and review the resulting hook after installation.

Risk: Commit subjects may be stored in .ctx-lockstep/commits.log.

Mitigation: Avoid using it on projects where commit subjects may contain sensitive information, or review and clear commits.log during checkpointing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/holdyounger/skills/ctx-lockstep)
- [README](README.md)
- [Initialization and testing guide](docs/初始化与测试说明.md)
- [Release specification](docs/发布规范.md)
- [Release notes and user guide](docs/发布说明与用户使用指南.md)
- [Project registry maintenance guide](docs/项目注册表维护说明.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON script arguments, and generated project context files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update .ctx-lockstep project files, workspace-level PROJECT_SYSTEM.md, checkpoints, commits.log, and a post-commit hook when initialized by the user.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
