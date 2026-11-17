## Description:

Brainstorm Beagle helps users turn fuzzy project ideas into concrete, implementation-free WHAT/WHY specifications through structured dialogue, context review, direction-setting, drafting, and self-review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product builders, and agent users use this skill to clarify an early project idea into a standalone specification before planning or implementation. It is especially suited to fuzzy feature or project concepts that need scope discipline, prior-art checking, and review for implementation leakage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read broad repository context while helping shape a specification.

Mitigation: Install and run it only in workspaces where broad context review is acceptable.

Risk: The skill can create a git commit without prominent, separate consent.

Mitigation: Require explicit approval before any commit, and ask the agent to show the target path and diff before saving or committing.

## Reference(s):

- [Spec Self-Review Checklist](references/spec-reviewer.md)
- [Spec Document Template](references/spec-template.md)
- [Brainstorm Beagle on ClawHub](https://clawhub.ai/anderskev/skills/brainstorm-beagle)
- [anderskev ClawHub Profile](https://clawhub.ai/user/anderskev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown specification document with conversational guidance and occasional shell commands for repository search or file operations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a WHAT/WHY project spec and avoids code, implementation plans, scaffolding, and other build actions.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
