## Description:

Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivansslo](https://clawhub.ai/user/ivansslo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill after implementation is complete to verify tests, inspect Git environment state, and choose a structured branch-completion workflow such as local merge, pull request creation, preservation, or discard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide actions that change local Git repository state, including merge, branch deletion, and worktree cleanup.

Mitigation: Review the presented workflow choice before execution, require explicit confirmation for discard, and verify tests before merge or PR actions.

Risk: Workspace cleanup can remove a worktree if ownership is misidentified.

Mitigation: Only remove worktrees under recognized `.worktrees/` or `worktrees/` paths and leave externally managed workspaces in place.

## Reference(s):

- [Server-resolved source import](https://github.com/ivansslo/Supwrs/tree/main/skills/finishing-a-development-branch)
- [ClawHub skill page](https://clawhub.ai/ivansslo/skills/finishing-a-development-branch-3)
- [Publisher profile](https://clawhub.ai/user/ivansslo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Git merge, push, branch deletion, and worktree cleanup commands only after test verification and user choice.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
