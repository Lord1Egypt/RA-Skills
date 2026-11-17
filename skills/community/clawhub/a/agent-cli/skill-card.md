## Description:

A routing and usage guide for Cursor CLI and Qoder CLI when agents need to modify code, refactor, review code, debug, or automate coding tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaohei2022](https://clawhub.ai/user/xiaohei2022)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to choose between Cursor CLI and Qoder CLI for code editing, refactoring, code review, debugging, CI automation, MCP-enabled tasks, worktree jobs, and subagent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation and automation shortcuts can run changing third-party code or bypass normal user review.

Mitigation: Review before installing, prefer verified package-manager installs over curl-to-bash, and review diffs before accepting generated changes.

Risk: Force or yolo modes and automatic workspace trust can allow broad code or shell changes without adequate confirmation.

Mitigation: Use these modes only for tightly scoped tasks, avoid auto-accepting workspace trust, and restrict tools and working directories.

Risk: MCP packages and CLI integrations can expand the execution surface beyond the base skill.

Mitigation: Pin and vet MCP packages before use, and configure allowed tools and denied tools for each project.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaohei2022/skills/agent-cli)
- [Agent CLI Installation and Index](references/README.md)
- [Cursor CLI Core Operations](references/cursorcli.md)
- [Qoder CLI Core Operations](references/qodercli.md)
- [Cursor CLI Install](https://cursor.com/install)
- [Qoder Documentation Index](https://docs.qoder.com/llms.txt)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes tool-selection guidance for Cursor CLI and Qoder CLI, with notes for TUI, tmux, permissions, MCP, and automation.]

## Skill Version(s):

3.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
