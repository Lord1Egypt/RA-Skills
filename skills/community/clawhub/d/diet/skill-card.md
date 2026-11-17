## Description:

Track food and nutrition. Use when logging meals, checking calories, tracking protein/carbs/fat, or generating diet reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to log meals, track calories, review protein, carbohydrate, fat, and water intake, and generate simple diet reports or meal plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meal, macro, calorie, and water-intake records are stored locally and may be readable by other local users if filesystem permissions are permissive.

Mitigation: Use owner-only permissions for ~/.diet and its JSON files, or install only on systems where local nutrition records can be stored with acceptable privacy controls.

Risk: Meal plans and nutrition reports rely on user-entered values and simple calculations, so they may be incomplete or unsuitable for health-sensitive decisions.

Mitigation: Review generated reports and plans before acting on them, and use qualified medical or nutrition advice for health-critical choices.

## Reference(s):

- [Diet skill page](https://clawhub.ai/ckchzh/skills/diet)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Plain text command output with local JSON data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores meal and water records locally under ~/.diet.]

## Skill Version(s):

3.4.1 (source: server release metadata; artifact frontmatter says 3.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
