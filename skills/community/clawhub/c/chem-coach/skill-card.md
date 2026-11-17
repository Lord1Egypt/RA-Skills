## Description:

Chem Coach AI is a Chinese Gaokao chemistry tutoring skill that classifies seven tutoring scenarios, guides students through chemistry questions, verifies equations, and supports reaction-mechanism analysis, beyond-syllabus translation, and seed practice questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abill6688](https://clawhub.ai/user/abill6688)

### License/Terms of Use:

MIT-0

## Use Case:

External students and education users use this skill for Chinese Gaokao chemistry tutoring across problem decomposition, solving, alternate methods, variations, general methods, mistake diagnosis, and guided coaching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad chemistry and exam-related trigger keywords may activate the skill when the user wanted a narrower chemistry workflow.

Mitigation: Use the security guidance to narrow trigger keywords or require explicit tutoring intent in deployments that need constrained activation.

Risk: The skill depends on chem-viz for visualization and can optionally use voice-coach or an IMA knowledge base; those dependencies may change the behavior seen by users.

Mitigation: Review and approve dependent skills and any configured IMA knowledge base separately before relying on those integrations.

Risk: Chemistry tutoring outputs can be misleading if equations, charges, electron transfer, or reaction conditions are wrong.

Mitigation: Preserve the artifact's four-layer equation verification and require review or rework when checks fail.

## Reference(s):

- [Chem Coach AI on ClawHub](https://clawhub.ai/abill6688/skills/chem-coach)
- [Publisher profile: abill6688](https://clawhub.ai/user/abill6688)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown/plain-text tutoring responses with worked chemistry explanations, guided questions, verification checklists, and optional visualization or knowledge-base handoff guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call for separate review of the hard chem-viz dependency and optional voice-coach or IMA knowledge-base integrations before deployment.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
