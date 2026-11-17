## Description:

Ai Companion Diet helps users track meals, steps, weight, calorie targets, reminders, and weight-loss trend analysis for diet planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeyoung310](https://clawhub.ai/user/joeyoung310)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to operate a local diet-tracking assistant that initializes user profile data, records meals, steps, and weight, and returns summaries, reminders, BMI/category calculations, plateau analysis, and trend predictions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive diet, step, and weight data in local JSON files.

Mitigation: Use it only in a trusted local environment and document data location, deletion, and file-permission behavior before deployment.

Risk: Unsafe input handling can execute local code when crafted meal, step, or weight values are supplied.

Mitigation: Avoid adversarial or copied values and prefer a fixed version that validates numeric inputs and passes data to Python as arguments instead of generated code.

Risk: Weight-loss recommendations may be mistaken for medical advice.

Mitigation: Present outputs as general wellness guidance and advise users with health conditions or discomfort to consult a qualified medical professional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joeyoung310/skills/ai-companion-diet)
- [ClawHub publisher profile](https://clawhub.ai/user/joeyoung310)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Terminal text with JSON data files and Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local JSON records under data/ and returns calorie, step, weight, reminder, and trend-analysis messages.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
