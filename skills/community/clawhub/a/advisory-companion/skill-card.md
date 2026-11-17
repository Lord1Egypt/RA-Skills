## Description:

A conversational advisory skill that helps people clarify personal, educational, career, family, and symbolic questions through structured interpretations and actionable next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals use the skill for conversational support and structured guidance across 11 advisory areas, including relationships, symbolic readings, education, health information, career planning, and parenting. It helps turn a clarified concern into practical next steps while directing crisis or out-of-scope issues to appropriate professional support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags sensitive client histories being carried across conversations without clear retention or deletion controls.

Mitigation: Use session-only handling, or agree explicitly on what may be saved, where, for how long, and how records can be reviewed and deleted; use read-only mode when writing is unnecessary.

Risk: Medical and psychological guidance may require professional review.

Mitigation: Keep professional boundaries clear and direct users to appropriate qualified support for diagnosis, treatment, or crisis needs.

## Reference(s):

- [Advisory Companion on ClawHub](https://clawhub.ai/wangjiaocheng/skills/advisory-companion)
- [Advisory Companion task catalog](artifact/references/advisory-companion-catalog.md)
- [Advisory Companion requirements](artifact/references/advisory-companion-requirements.md)
- [Advisory Companion exemplars](artifact/references/advisory-companion-exemplars.md)
- [Interpretation report template](artifact/templates/解读报告模板.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational responses and structured Markdown interpretations, plans, and scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Layered observations, explanations, recommendations, and boundaries; includes a practical next step and labels uncertainty where relevant.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
