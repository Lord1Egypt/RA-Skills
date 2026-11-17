## Description:

Generates Bazi (Four Pillars) charts and personalized fortune-telling interpretations across eight life domains, with optional Zi Wei Dou Shu cross-checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laurc2004](https://clawhub.ai/user/laurc2004)

### License/Terms of Use:

MIT

## Use Case:

External users can ask an agent to calculate a traditional Bazi chart from birth details, check Chinese calendar dates, and prepare a personalized reading of family, health, career, finances, relationships, social life, education, and spirituality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reading requests precise birth details and sensitive family and life-event information.

Mitigation: Share only necessary details; avoid names and third-party family information.

Risk: The workflow calls for saving a sensitive reading to a TXT file without stated privacy controls.

Mitigation: Do not save the report unless the user requests it and chooses a safe location.

Risk: Health, legal, and financial interpretations may be mistaken for professional advice.

Mitigation: Treat these outputs as cultural or entertainment analysis, not a substitute for qualified advice.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/laurc2004/skills/bazi-full-fortune)
- [Bazi fundamentals](references/bazi-fundamentals.md)
- [Analysis guide](references/analysis-guide.md)
- [Interview guide](references/interview.md)
- [cantian-tymext charting dependency](https://www.npmjs.com/package/cantian-tymext)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown reading and UTF-8 TXT report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes chart data and an eight-domain interpretation; optional Zi Wei Dou Shu cross-check.]

## Skill Version(s):

1.1.5 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
