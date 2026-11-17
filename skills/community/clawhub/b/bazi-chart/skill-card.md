## Description:

Professional BaZi (八字) chart calculator and analysis tool that calculates Four Pillars of Destiny from birth date, time, and location, including solar terms, true solar time correction, hidden stems, ten gods, five elements, major luck periods, and relationship analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reed1898](https://clawhub.ai/user/reed1898)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to calculate BaZi birth charts from date, time, location, and gender inputs, then present text or JSON analysis for Chinese metaphysics workflows. It is intended for chart calculation and interpretive assistance, not for deterministic life, financial, medical, or legal decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Birth date, birth time, location, and gender can be sensitive personal details.

Mitigation: Ask for and process only the details needed for the requested chart, and avoid retaining or sharing the input outside the local calculation workflow.

Risk: The skill installs the external ephem dependency, which may introduce supply-chain risk if installed broadly or without version controls.

Mitigation: Install in an isolated virtual environment, avoid administrator-level pip installs, and pin or hash-lock ephem before production use.

Risk: BaZi astrology output may be mistaken for certain prediction or professional advice.

Mitigation: Present results as Chinese metaphysics interpretation and avoid using the chart as a substitute for medical, legal, financial, or other professional judgment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/reed1898/skills/bazi-chart)
- [Publisher profile](https://clawhub.ai/user/reed1898)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text chart output or structured JSON from a local CLI, usually summarized to the user in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Consumes birth date, birth time, city or coordinates, gender, optional annual luck year, and optional true solar time correction toggle.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
