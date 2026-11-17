## Description:

Multi Agent provides design patterns for choosing coordinator, fork, or swarm workflows and for coordinating multi-agent work with task files, file locks, worktree isolation, synthesis gates, and independent review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to plan and coordinate multi-agent coding or review workflows, including mode selection, task claiming, workspace isolation, synthesis before implementation, and independent verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill discusses sending task descriptions, diffs, review results, and synthesis files to Claude-based agents, which may expose secrets or proprietary content.

Mitigation: Review and redact prompts, diffs, coordination files, and generated outputs before sending them to an external model, and use only approved providers.

Risk: The examples include mutating git worktree, merge, branch deletion, lock cleanup, and hook workflows that can affect a repository if copied without safeguards.

Mitigation: Treat commands as manual patterns; scope them to disposable branches or isolated worktrees, inspect paths and branch names, and require human review before destructive cleanup or merge operations.

Risk: The authoritative security verdict is suspicious because the guidance lacks sufficient scoping, redaction, and safety controls for multi-agent workflows.

Mitigation: Install only for Claude-based multi-agent workflows where operators can review each command and adapt safeguards to the project.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanyasheng/skills/eh-multi-agent)
- [Delegation Modes](references/delegation-modes.md)
- [Task Coordination](references/task-coordination.md)
- [File Claim Lock](references/file-claim-lock.md)
- [Workspace Isolation](references/workspace-isolation.md)
- [Synthesis Gate](references/synthesis-gate.md)
- [Review-Execution Separation](references/review-execution-separation.md)
- [Extended Patterns](references/extended-patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline shell, JSON, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory coordination patterns and examples that require project-specific review before use.]

## Skill Version(s):

2.4.0 (source: server release metadata; artifact frontmatter and metadata.json report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
