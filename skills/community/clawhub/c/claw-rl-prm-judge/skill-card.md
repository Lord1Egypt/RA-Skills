## Description:

Evaluates AI agent turns across six quality dimensions and returns structured scores and feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huanmeng9527](https://clawhub.ai/user/huanmeng9527)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to review agent turns, investigate regressions, and compare quality across intent, reasoning, tool use, safety, efficiency, and user value.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent traces sent to a judge or stored for review may contain personal data or credentials.

Mitigation: Redact sensitive inputs and tool results before judging or persistence; avoid storing credentials.

Risk: A single judge score can mislead automated policy, training, or guard changes.

Mitigation: Review per-dimension scores and use human oversight and independent checks before changing agent behavior.

Risk: Automatic activation on user corrections may evaluate a turn when no review was intended.

Mitigation: Prefer explicit invocations when reviewing agent quality.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huanmeng9527/skills/claw-rl-prm-judge)
- [Six-dimension scoring rubric](references/dimensions.md)
- [Judge prompt example](examples/judge-prompt.md)
- [Score storage guidance](references/storage-schema.md)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [JSON evaluation with six dimension scores and a brief summary; Markdown rubric and storage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores range from 0.0 to 1.0 per dimension; an optional composite summarizes them.]

## Skill Version(s):

1.0.6 (source: server-resolved ClawHub release; artifact frontmatter says 1.0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
