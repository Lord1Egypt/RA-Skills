## Description:

AKM Fitness helps an agent model fitness goals, body limits, equipment context, time budget, recovery, and adherence risks before producing a constraint-aware training decision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sirsws](https://clawhub.ai/user/sirsws)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill to turn fitness goals, physical constraints, equipment availability, time limits, and recovery state into a structured training profile and a practical workout decision. It is intended for constraint-aware planning, not diagnosis, rehabilitation care, or broad medical guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for health-related and body-limitation details that may be sensitive.

Mitigation: Share only the details needed for planning and avoid unnecessary medical history or identifying information.

Risk: Fitness output could be mistaken for medical diagnosis or rehabilitation care.

Mitigation: Use the skill as a training decision aid and defer diagnosis, rehabilitation planning, and medical restrictions to a qualified clinician.

Risk: The install command uses a mutable npx/GitHub source.

Mitigation: Review the resolved repository contents before installation and prefer a pinned commit or verified release when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sirsws/skills/akm-fitness-planner)
- [Public sample record](https://github.com/sirsws/akm/blob/main/branches/fitness/skill/SAMPLE_RECORD.md)
- [AKM fitness branch paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6231465)
- [Skill source files](https://github.com/sirsws/akm/tree/main/branches/fitness/skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured fields and YAML-style examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a training profile, state judgment, primary decision, confidence, plan, risk notes, non-negotiables, and missing inputs.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
