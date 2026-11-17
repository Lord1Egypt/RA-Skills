## Description:

This skill guides agents through conversational feature requirements clarification and produces TDD-ready acceptance criteria before implementation work begins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cping6](https://clawhub.ai/user/cping6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and independent builders use this skill to turn vague feature ideas into scoped requirements documents with numbered Given-When-Then acceptance criteria before starting implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted project context can steer the agent outside the intended requirements-clarification scope.

Mitigation: Use this skill with trusted repositories or review specs/PROJECT-CONTEXT.md before invocation, and keep the final requirements focused on observable product behavior.

Risk: The workflow is written for a Chinese-language requirements process, which can make review harder for teams that do not read Chinese.

Mitigation: Have a qualified reviewer check the generated Markdown requirements before using them as implementation or test-planning input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cping6/skills/feature-requirements-clarification)
- [Feature requirements template](assets/feature-requirements-template.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files]

**Output Format:** [Conversational guidance followed by a Markdown requirements document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final documents are intended for specs/features/[feature-name].md after user confirmation.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
