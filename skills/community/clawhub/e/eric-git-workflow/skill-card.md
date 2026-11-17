## Description:

Provides Git workflow guidance for branching strategies, commit conventions, merge and rebase workflows, conflict resolution, CI/CD integration, and recovery from common mistakes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlooi504](https://clawhub.ai/user/ericlooi504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose Git branching models, write conventional commits, resolve merge or rebase conflicts, clean commit history, configure common aliases or commit templates, and recover from common Git mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes destructive Git command examples that can discard local work or rewrite shared history if executed without review.

Mitigation: Require explicit confirmation before destructive Git operations, check `git status` first, avoid force-pushing shared or protected branches, and prefer safer recovery commands such as `git revert` when appropriate.

## Reference(s):

- [Git Workflow Patterns](references/workflows.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
