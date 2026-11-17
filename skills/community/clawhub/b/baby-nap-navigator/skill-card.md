## Description:

Helps caregivers plan age-based nap windows and bedtime from logged wake times, with schedule projections, drift checks, and weekly summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Caregivers use this skill to estimate nap and bedtime windows, review changing nap patterns, and share a daily or weekly sleep plan. It is scheduling guidance, not medical or sleep-training advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Caregiver-entered infant sleep data is stored locally in plain JSON and may be visible to others with access to the file.

Mitigation: Use the default state file or a dedicated path and limit access to the local data.

Risk: Choosing an important file as the state path could overwrite its contents.

Mitigation: Do not point --state at important files; use a dedicated state file.

Risk: A projected nap schedule could be mistaken for individualized medical advice.

Mitigation: Treat output as scheduling help only, follow the included safe-sleep guidance, and consult a pediatrician about concerning symptoms.

## Reference(s):

- [Baby Nap Navigator on ClawHub](https://clawhub.ai/voronindenis5/skills/baby-nap-navigator)
- [Wake-Window Science & Nap Transitions](references/wake-window-science.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain-text nap schedules, timing windows, drift assessments, and weekly summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans include safe-sleep reminders and a medical-advice disclaimer; caregiver logs are saved locally as JSON.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
