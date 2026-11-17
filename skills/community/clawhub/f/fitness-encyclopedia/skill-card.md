## Description:

Fitness Encyclopedia is an AI fitness assistant for personalized training plans, nutrition calculation, strength prediction, joint assessment, and general fitness knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emilyyangmm](https://clawhub.ai/user/emilyyangmm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and fitness-focused agents use this skill to collect relevant user details, generate training and nutrition guidance, estimate strength, and adapt recommendations around joint limitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate broadly on fitness-related wording and collect personal body, diet, and joint or injury details.

Mitigation: Install only in contexts where this data collection is expected, and tell users what information is needed before they provide sensitive details.

Risk: Nutrition, injury, and rehabilitation suggestions could be mistaken for medical advice.

Mitigation: Present outputs as general fitness guidance and direct users to qualified health professionals for medical, injury, rehabilitation, or dietary decisions.

Risk: Calorie, macro, and strength estimates may be inaccurate for an individual user.

Mitigation: Review calculated results before relying on them and treat them as estimates that require user-specific adjustment.

Risk: Mutable latest install commands can change what code is installed over time.

Mitigation: Prefer a pinned and reviewed release version for deployment.

## Reference(s):

- [Training Plans](references/training_plans.md)
- [Food Nutrition](references/food_nutrition.md)
- [Cardio Calories](references/cardio_calories.md)
- [Muscle Stretching](references/muscle_stretching.md)
- [Muscle Anatomy](references/muscle_anatomy.md)
- [Joint Movements](references/joint_movements.md)
- [Joint Limited Guide](references/joint_limited_guide.md)
- [User Interaction Guide](references/user_interaction_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown or plain text with optional script-backed calculation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for personal body, diet, schedule, and joint or injury details before producing personalized recommendations.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
