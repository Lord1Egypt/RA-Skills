## Description:

Auto-selects which skills to load for the current user turn and outputs ranked recommendations with one-line reasons and an opt-in `/autoselect` slash trigger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fvegiard](https://clawhub.ai/user/fvegiard)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to evaluate a user turn against available skills and produce ranked recommendations for which skills to load. The recommendations are advisory and the invoking agent remains responsible for deciding what to load.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest loading other skills automatically, which can add unwanted context or noise when manual skill selection is preferred.

Mitigation: Review the trigger breadth before deployment and keep recommendations advisory so the agent decides whether to load suggested skills.

## Reference(s):

- [Source repository](https://github.com/fvegiard/autoselect-skill)
- [ClawHub skill page](https://clawhub.ai/fvegiard/skills/autoselect-skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style structured recommendation block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ranked skill names, scores, one-line reasons, ignored skills, and a suggested next action.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
