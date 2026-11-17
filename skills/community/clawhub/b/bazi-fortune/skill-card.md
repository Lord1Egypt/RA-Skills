## Description:

Bazi Fortune generates Chinese Four Pillars astrology charts and interpretive reports from a user's birth date, birth time, and sex using deterministic chart calculations plus LLM-based synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eamanc-lab](https://clawhub.ai/user/eamanc-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request Bazi chart calculation, Five Elements and Ten Gods analysis, major luck-cycle and annual-flow readings, and concise answers to targeted fortune-analysis questions. The skill is intended for entertainment and self-exploration, not medical, legal, financial, or other professional decision-making.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may silently reuse or store birth date, birth time, sex, optional birthplace, and derived fortune-profile data in local MEMORY.md files.

Mitigation: Use it in a private workspace, obtain user consent before storing or reusing profile data, and delete or avoid creating MEMORY.md when session-only use is desired.

Risk: Fortune-telling interpretations can be mistaken for professional medical, legal, financial, or life-decision advice.

Mitigation: Present outputs as entertainment and self-exploration, retain the artifact's professional-advice disclaimer, and direct users to qualified professionals for high-stakes decisions.

## Reference(s):

- [Bazi chart calculation rules](references/calculation-rules.md)
- [Bazi interpretation guide](references/interpretation-guide.md)
- [Project homepage](https://github.com/eamanc-lab/fortune-telling-skills)
- [ClawHub skill page](https://clawhub.ai/eamanc-lab/skills/bazi-fortune)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Files, Guidance]

**Output Format:** [Markdown reports with tables, calculation traces, and concise text answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read from and write to local MEMORY.md files containing birth-profile data and derived chart cache.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
