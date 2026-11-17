## Description:

Dining helps an agent decide what users should eat by producing concrete meal plans for home cooking, dining out, delivery, gatherings, fitness goals, and special dining scenarios while accounting for dietary restrictions and health red lines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchen913](https://clawhub.ai/user/chenchen913)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when they want an agent to choose meals or menus instead of presenting broad options. It supports everyday meal planning, delivery selection, home-cooking schedules, gatherings, special scenarios such as hot pot or camping, and fitness-oriented meal recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented npx install command is unpinned, so users may install a moving version without review.

Mitigation: Install from a pinned release or reviewed commit before deployment.

Risk: The optional preference profile may include sensitive dietary or medical details that users paste into future sessions.

Mitigation: Keep sensitive health details out of reusable profiles unless the user is comfortable reusing that information in later agent sessions.

Risk: Health-related meal recommendations may be mistaken for medical advice.

Mitigation: Treat outputs as dietary guidance and consult qualified medical or nutrition professionals for clinical conditions.

## Reference(s):

- [Mode Routing](artifact/references/mode-routing.md)
- [Algorithm Engine](artifact/references/algorithm-engine.md)
- [Cuisine Profiles](artifact/references/cuisine-profiles.md)
- [Expert Cabinet](artifact/references/expert-cabinet.md)
- [Memory System](artifact/references/memory-system.md)
- [Output Schema](artifact/references/output-schema.md)
- [Heuristics](artifact/references/heuristics.md)
- [Dishes Reference](artifact/assets/dishes-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown meal plans with dish lists, concise rationale, and optional cooking schedule, delivery notes, expert review, or preference-profile update text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs usually provide one or two concrete meal solutions and avoid vague alternatives unless a constraint conflict requires user clarification.]

## Skill Version(s):

2.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
