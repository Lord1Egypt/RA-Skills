## Description:

Estimate calorie content from food names, portion sizes, or food images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rajib76](https://clawhub.ai/user/rajib76)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to estimate calories for individual foods, full meals, or uploaded food images. The skill is intended to provide approximate per-item and total calories, with assumptions stated when portions or preparation details are unclear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calorie and macronutrient estimates can be inaccurate for homemade meals, mixed dishes, unclear portion sizes, or visually ambiguous food images.

Mitigation: State assumptions clearly, present estimates or ranges rather than exact values, and call out low confidence when image or portion evidence is weak.

Risk: Uploaded food images may reveal personal context beyond the meal itself.

Mitigation: Ask users to share only images they are comfortable having analyzed in the agent environment.

## Reference(s):

- [Calorie Compass on ClawHub](https://clawhub.ai/rajib76/skills/calorie-compass)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise natural-language calorie estimates, often as Markdown lists or short paragraphs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes stated assumptions, possible calorie ranges, per-item and total calories, confidence notes for image-based estimates, and optional macronutrient estimates when enough detail is available.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
