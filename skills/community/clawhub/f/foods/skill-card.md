## Description:

Analyzes a user's meal or daily food intake and gives gentle, general feedback on dietary balance, portion coverage, and approximate calorie or nutrient limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to review meals, snacks, or a full day of eating against Asian dietary guidance and receive concise, non-clinical suggestions for improving balance.

### Deployment Geography for Use:

Asia

## Known Risks and Mitigations:

Risk: Users may treat general nutrition feedback as individualized medical or clinical diet advice.

Mitigation: Keep advice general and non-clinical, and direct users with chronic conditions, pregnancy, allergies, eating-disorder concerns, or individualized dietary needs to qualified clinicians or dietitians.

Risk: Vague meal descriptions can make portion and calorie estimates unreliable.

Mitigation: Ask for portion details when needed and clearly label calorie estimates as approximate.

Risk: The guidance is scoped mainly to Asian populations or people living in Asia and uses regional serving systems.

Mitigation: State the scope when relevant and avoid presenting regional serving recommendations as universal clinical standards.

## Reference(s):

- [Nutrition Serving (SV) Guide](references/nutrition_sv_guide.md)
- [The Food Pyramid - A Guide to a Balanced Diet](references/balanced_diet_hk.md)
- [Centre for Health Protection, Hong Kong - The Food Pyramid](https://www.chp.gov.hk/en/static/90017.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown prose with short bullet suggestions and approximate calorie notes when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [General nutrition guidance only; typical responses are concise unless the user requests a detailed breakdown.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
