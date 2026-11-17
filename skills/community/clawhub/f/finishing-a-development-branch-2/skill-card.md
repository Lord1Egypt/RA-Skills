## Description:

Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovemymobilewebsite-dotcom](https://clawhub.ai/user/lovemymobilewebsite-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to finish completed development branches by verifying tests, identifying a base branch, and choosing a merge, pull request, keep, or discard workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct worktree cleanup after pull request creation, which can remove a worktree the user expected to keep.

Mitigation: Before using the pull request path, confirm that the worktree should be preserved unless the user explicitly requests cleanup.

Risk: Worktree removal can discard local context if the worktree is not clean or the user has not confirmed deletion.

Mitigation: Require explicit confirmation and a clean-worktree check before removing a worktree.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown with inline shell commands and pull request body templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the agent to verify tests before merge or pull request workflows and to request typed confirmation before discarding work.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
