## Description:

A 7-step problem-solving discipline loop that gives any model structured thinking: classify the ask, define done, gather evidence, decide, act surgically, verify by observation, report outcome-first.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plato-1](https://clawhub.ai/user/plato-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent operators use this skill to apply a disciplined reasoning and verification loop to non-trivial questions, debugging work, refactors, and behavior changes under uncertainty.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation guidance can add process overhead and extra tool use to multi-step tasks.

Mitigation: Use the skill for non-trivial work and apply its triviality gate to skip the loop for small, obvious changes.

Risk: The skill can shape agent reasoning and recommendations, so poor application may still produce incorrect or misleading guidance.

Mitigation: Follow the skill's verification step and review the resulting answer or change before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Markdown guidance with structured workflow steps and optional inline code or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code; output depends on the agent task being planned, audited, performed, or reported.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
