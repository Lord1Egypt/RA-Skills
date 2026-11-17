## Description:

Manage Git worktrees for isolated parallel development, including creating, listing, switching, and cleaning up worktrees for concurrent reviews or feature work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this tool to create, inspect, switch among, and clean up isolated Git worktrees for parallel feature work and code review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating a worktree from a trusted base can copy .env files into it.

Mitigation: Use --no-env for untrusted bases and review copied environment files before using the new worktree.

Risk: Setup may install dependencies or run project-specific setup actions.

Mitigation: Inspect the base repository and follow the skill's trust-specific setup guidance before running installs.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/iliaal/skills/compound-eng-git-worktree)
- [Workflow examples](artifact/references/workflow-examples.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [Worktree integration](artifact/references/worktree-integration.md)
- [Commit ownership](artifact/references/commit-ownership.md)
- [Hooks and local excludes](artifact/references/hooks-and-excludes.md)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Git worktree lifecycle instructions and safety guidance.]

## Skill Version(s):

5.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
