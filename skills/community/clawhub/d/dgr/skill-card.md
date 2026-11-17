## Description:

This superseded reference skill produces structured JSON decision records with assumptions, risks, recommendations, and consistency checks for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dgr-ai-labs](https://clawhub.ai/user/dgr-ai-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and decision reviewers use this reference skill to document decision context, assumptions, risks, and recommendations in a consistent format for human review. It does not enforce actions or establish that a recommendation is correct.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A structured rationale can be mistaken for verified evidence or a correct decision.

Mitigation: Validate important assumptions and sources independently, and require qualified human review before acting on high-stakes recommendations.

Risk: The skill documents decisions but cannot prevent an agent from taking an unsafe action.

Mitigation: Do not treat the record as an enforcement mechanism; apply separate controls before consequential actions.

## Reference(s):

- [DGR skill release](https://clawhub.ai/dgr-ai-labs/skills/dgr)
- [DGR Gate successor](https://clawhub.ai/dgr-ai-labs/plugins/openclaw-dgr-gate)
- [Decision record schema](artifact/schema.json)
- [Decision record field guide](artifact/field_guide.md)

## Skill Output:

**Output Type(s):** [Structured decision records]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes assumptions, risks, a recommendation, and a consistency check; intended for human review, not enforcement.]

## Skill Version(s):

1.1.1 (source: ClawHub release evidence; bundled SKILL.md states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
