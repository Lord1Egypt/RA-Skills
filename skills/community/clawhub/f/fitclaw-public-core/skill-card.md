## Description:

FitClaw Public Core provides a public-safe AI fitness coaching workflow for onboarding, hydration, nutrition, and training structure without exposing private user data or live production configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beachanger](https://clawhub.ai/user/beachanger)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to run a reusable AI fitness coaching workflow for lightweight onboarding, hydration habits, practical nutrition guidance, and training-plan structure while keeping private FitClaw data out of the package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to retain health-adjacent fitness, body, nutrition, or habit information without clear consent, retention, or deletion controls.

Mitigation: Before installation, configure the agent to ask before saving health-adjacent details, store only necessary information, and tell users how remembered data can be reviewed or deleted.

Risk: Nutrition, hydration, and training outputs can be mistaken for precise medical or individualized professional advice.

Mitigation: Keep coaching language practical and uncertainty-aware, label estimates as estimates, and avoid exact prescriptions when baseline data is incomplete.

## Reference(s):

- [FitClaw Onboarding Public](references/fitclaw-onboarding-public.md)
- [FitClaw Hydration Public](references/fitclaw-hydration-public.md)
- [FitClaw Nutrition Public](references/fitclaw-nutrition-public.md)
- [FitClaw Training Public](references/fitclaw-training-public.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown coaching guidance, structured checklists, and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should label estimates as estimates and avoid exact prescriptions when baseline data is incomplete.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
