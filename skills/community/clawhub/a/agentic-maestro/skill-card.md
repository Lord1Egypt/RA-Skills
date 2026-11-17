## Description:

Coordinates coding-agent delegation through precise briefs, independent review, and a build–review–fix–merge workflow across Claude Code, Codex, and OpenCode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akramovic1](https://clawhub.ai/user/akramovic1)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to delegate scoped coding tasks to agent executors, review their work independently, and integrate verified changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write-mode coding agents can modify repository files.

Mitigation: Run write-mode agents in disposable git worktrees and review scope-check results before committing.

Risk: A headless agent review or scout could receive unnecessary write access.

Mitigation: Use read-only mode for reviews and scouting.

Risk: OpenCode write mode does not provide an OS sandbox.

Mitigation: Use a disposable worktree and assess the execution environment before enabling write mode.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/akramovic1/skills/agentic-maestro)
- [Agent harnesses](references/harnesses.md)
- [Operations guide](references/operations.md)
- [Pre-review checklist](references/checklist.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown briefs and reviews with code and shell commands as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scoped implementation changes and verification reports from delegated agents.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
