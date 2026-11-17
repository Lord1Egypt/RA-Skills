## Description:

开发者十二铁律 + 开发规范 + 高级调试方法论 — 开发者核心技能（合并自 diagnose）

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyunss](https://clawhub.ai/user/liuyunss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as Chinese-language guidance for AI-assisted software development, debugging workflows, code review, and implementation discipline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest persistent services or long-running background jobs.

Mitigation: Require explicit user approval for the exact command, restart policy, log location, and cleanup plan before starting persistent or background processes.

Risk: The skill may suggest remote file transfer or remote host changes.

Mitigation: Require explicit user approval for the exact files, commands, destinations, and remote host before transferring files or changing remote systems.

Risk: The skill may suggest package installation without sufficient pinning.

Mitigation: Use pinned package versions and review installation commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuyunss/skills/developer-skills)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with checklists and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primarily Chinese-language developer guidance; outputs should be reviewed before acting on commands or operational changes.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
