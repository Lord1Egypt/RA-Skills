## Description:

Use the forktree Python CLI to safely create, list, remove, and garbage-collect git worktrees from a shell pipeline, CI job, or unattended coding agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bottanicals](https://clawhub.ai/user/bottanicals)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, CI maintainers, and coding agents use this skill to operate the external forktree CLI for creating, listing, removing, and garbage-collecting Git worktrees with predictable stdout, stderr, configuration, and exit-code behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides agents to use an external CLI that can create, remove, and garbage-collect Git worktrees.

Mitigation: Install it only when worktree management is intended, review the CLI provenance separately, and prefer dry-run or non-force modes before destructive cleanup.

Risk: Incorrect control flow could ignore stderr or non-zero exits and continue with an empty or invalid worktree path.

Mitigation: Check the forktree exit code, read stderr before retrying, and only change directories after a successful stdout path is returned.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/BottaniCals/agent-skills/tree/main/skills/forktree)
- [forktree project homepage](https://github.com/BottaniCals/forktree)
- [ClawHub skill page](https://clawhub.ai/bottanicals/skills/forktree)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands, command-output contracts, configuration notes, and exit-code guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance assumes the external forktree binary is installed and available on PATH.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
