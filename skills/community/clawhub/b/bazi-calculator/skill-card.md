## Description:

Calculates Four Pillars BaZi values from a birth date and time using a trusted reference datetime, with optional DaYun luck cycles and current LiuNian Ganzhi output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wingchiu](https://clawhub.ai/user/wingchiu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to calculate BaZi pillars, eight characters, DaYun cycles, and current LiuNian values from birth details and a verified reference dataset.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Birth date, time, and timezone can be sensitive personal data.

Mitigation: Run the calculator locally and avoid sharing birth details or outputs beyond the intended analysis context.

Risk: The calculator depends on the local Python environment and the lunar_python library.

Mitigation: Confirm Python and lunar_python are installed before use, and treat dependency installation as a separate environment setup step.

Risk: BaZi accuracy depends on the selected reference data and boundary rules.

Mitigation: Use verified JiaZi anchors or reference data, and validate outputs against a trusted almanac source when precision matters.

## Reference(s):

- [Anchor Requirements](references/method.md)
- [Verified Reference Dataset](references/reference-verified.json)
- [Reference Template](references/reference-template.json)
- [Anchor Template](references/anchors-template.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and plain text calculation output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calculations depend on birth datetime, timezone, reference JSON, and optional gender for DaYun.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
