## Description:

CodeFlicker CLI programming assistant for Kuaishou employees that helps agents install, configure, and delegate coding tasks to flickcli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegodamn](https://clawhub.ai/user/leegodamn)

### License/Terms of Use:

MIT

## Use Case:

Developers and coding agents use this skill to check, configure, and run Kuaishou's CodeFlicker CLI for implementation, debugging, refactoring, code review, session continuation, and git-worktree workspace workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates development work to CodeFlicker under the user's Kuaishou account.

Mitigation: Install and use it only when delegation to CodeFlicker under that account is intended.

Risk: Persistent global auto-execute mode can allow broad unattended edits or command execution.

Mitigation: Keep approvalMode at default for normal work and reserve yolo mode for disposable, isolated workspaces.

Risk: Workspace completion, workspace deletion, MCP additions, and natural-language shell execution are high-impact actions.

Mitigation: Review those actions before execution and avoid running them against important repositories without isolation.

Risk: The CLI package is installed from an internal npm registry.

Mitigation: Pin or otherwise verify the CLI package where possible before installing or updating it.

## Reference(s):

- [ClawHub Codeflicker release page](https://clawhub.ai/leegodamn/skills/codeflicker)
- [Publisher profile](https://clawhub.ai/user/leegodamn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegates requested coding work to flickcli and may create, edit, merge, or delete workspace files depending on CodeFlicker configuration.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
