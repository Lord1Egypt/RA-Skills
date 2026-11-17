## Description:

Aistro provides professional astrology consultation, personalized horoscope guidance, and report generation for natal charts, daily predictions, synastry compatibility, and moon phase readings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lban2049](https://clawhub.ai/user/lban2049)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use Aistro to ask astrology questions and generate personalized reports based on birth details, target dates, compatibility inputs, and moon phase calculations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for birth date, birth time, birth place, and, for synastry, another person's birth details.

Mitigation: Ask only for details needed for the requested report, avoid entering another person's birth details without permission, and treat birth information as sensitive chat context.

Risk: The skill may run npm install for local calculation scripts.

Mitigation: Review the packaged dependencies and lockfile before installation when strict reproducibility or dependency review is required.

Risk: Personalized astrology output can be mistaken for professional life, health, relationship, or financial advice.

Mitigation: Frame readings as reflective astrology guidance and avoid presenting them as a substitute for qualified professional advice.

## Reference(s):

- [Natal Chart Report](references/natal-report.md)
- [Horoscope Prediction Report](references/predict-report.md)
- [Synastry Report](references/synastry-report.md)
- [Moon Phase Report](references/moon-phase-report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Conversational text and Markdown reports with inline shell commands for local astrology calculation scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require birth date, birth time, birth place, target date, and second-person birth details for synastry; outputs in the user's language.]

## Skill Version(s):

0.1.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
