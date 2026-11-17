## Description:

Guides agents through project context review, clarifying questions, option comparison, design approval, and written specification before implementation planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivansslo](https://clawhub.ai/user/ivansslo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to turn feature or behavior-change requests into reviewed designs and written specifications before implementation planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly gate implementation work and redirect small changes into a required design and specification workflow.

Mitigation: Install it only where explicit design approval gates are desired, and review the workflow expectations before enabling it for routine coding tasks.

Risk: The skill can cause repository changes and commits as part of brainstorming.

Mitigation: Run it in a controlled workspace and review generated specification files and commits before accepting them.

Risk: The skill may prevent other suitable implementation skills from being used until its workflow completes.

Mitigation: Use it for planning-heavy work and disable or override it when immediate implementation is the intended behavior.

## Reference(s):

- [Server-resolved source repository](https://github.com/ivansslo/Supwrs/tree/main/skills/brainstorming)
- [ClawHub skill listing](https://clawhub.ai/ivansslo/skills/brainstorming-6)
- [Publisher profile](https://clawhub.ai/user/ivansslo)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown prose with structured design sections and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update a design document before implementation planning.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
