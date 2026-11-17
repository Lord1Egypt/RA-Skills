## Description:

Use when a written implementation plan is ready to execute, when the user says "fire", "execute the plan", "build it", or hands over a plan file to implement. The step after recipe.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to execute a written coding plan in discrete tasks on an isolated branch or worktree, with verification checkpoints and commits. The user reviews the plan before execution and chooses what to do with the completed work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A plan may contain incorrect or misleading guidance, and the skill executes tasks and creates commits without pausing between them.

Mitigation: Review the full plan and repository state before execution, assess companion skills separately, and verify the completed work before choosing its final disposition.

## Reference(s):


## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Guidance, Markdown]

**Output Format:** [Code and file changes, shell commands, and concise Markdown task and verification summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task-by-task execution with verification checkpoints and commits; final disposition remains user-selected.]

## Skill Version(s):

1.0.1 (source: target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
