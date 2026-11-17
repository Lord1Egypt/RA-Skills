## Description:

Calculates Body Mass Index, DuBois Body Surface Area, basic BMI category, and optional BSA-based dose values from local height and weight inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a local BMI/BSA calculator for basic anthropometric screening examples and simple BSA-based dose arithmetic. Clinical or medication decisions require independent validation before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinical documentation overstates supported pediatric, multi-formula, AUC, dose-cap, and reporting capabilities relative to the implementation.

Mitigation: Treat outputs as unvalidated examples and rely only on the implemented BMI, DuBois BSA, and simple BSA dose arithmetic unless the implementation is corrected and independently validated.

Risk: BMI, BSA, and dose calculations may be misused for real clinical or medication decisions.

Mitigation: Require qualified clinical review, confirm units and formulas, and independently double-check all medication or chemotherapy calculations before use.

Risk: The requirements file lists Python standard-library modules and may be misleading as an installation source.

Mitigation: Do not rely on requirements.txt for package installation; review the script directly and run it in a controlled Python environment.

## Reference(s):

- [BMI & BSA Calculator - References](references/guidelines.md)
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/bmi-bsa-calculator)
- [Publisher profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, files]

**Output Format:** [Plain text or JSON CLI output, with optional file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts weight, height, optional dose, output format, and output path parameters.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
