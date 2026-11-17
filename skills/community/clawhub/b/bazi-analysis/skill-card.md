## Description:

Professional Bazi / Four Pillars consultation skill for birth date and time analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spyfree](https://clawhub.ai/user/spyfree)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to produce Bazi / Four Pillars birth-chart reports from birth date, birth time, and gender. It supports chart facts, five-element balance, luck-cycle and yearly outlook summaries, and practical consultation-style interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes birth date, birth time, and gender inputs, which can be personal data.

Mitigation: Run the charting script locally and avoid exposing it directly to untrusted users.

Risk: Bazi output is traditional metaphysical interpretation and may be mistaken for professional advice.

Mitigation: Present outputs as metaphysical analysis only and retain the medical, legal, and investment advice disclaimer.

Risk: Unbounded yearly outlook generation can increase runtime or output size if exposed as a service.

Mitigation: Bound the --years parameter and supported year ranges when integrating the script into user-facing systems.

## Reference(s):

- [Bazi Analysis on ClawHub](https://clawhub.ai/spyfree/skills/bazi-analysis)
- [Publisher profile: spyfree](https://clawhub.ai/user/spyfree)
- [notes.md](references/notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown consultation report or structured JSON generated from local chart inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires birth date, birth time, and gender; optional sect, start year, year count, and output format parameters.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
