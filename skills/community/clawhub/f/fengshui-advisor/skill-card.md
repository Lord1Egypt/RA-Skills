## Description:

Fengshui Advisor analyzes Eight Mansions and Xuan Kong Flying Star feng shui using birth year, sex, and optional home orientation to produce directional auspiciousness, Flying Star charts, and layout guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eamanc-lab](https://clawhub.ai/user/eamanc-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to generate Chinese-language feng shui reports, directional consultations, and space layout recommendations from personal birth-year/sex inputs and optional residence orientation details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist birth year, sex, residence details, and derived feng shui classifications in local memory.

Mitigation: Use only where cross-session profile storage is acceptable, or require explicit confirmation before writing MEMORY.md and minimize stored fields.

Risk: The skill can reuse another fortune-hub memory profile without clear user consent.

Mitigation: Require explicit consent before reading external memory and confirm imported fields with the user before use.

Risk: Feng shui recommendations may be mistaken for professional medical, legal, financial, or structural advice.

Mitigation: Keep outputs framed as entertainment and self-exploration, and direct users to qualified professionals for regulated or structural decisions.

## Reference(s):

- [Calculation Rules](references/calculation-rules.md)
- [Interpretation Guide](references/interpretation-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/eamanc-lab/skills/fengshui-advisor)
- [Project Homepage](https://github.com/eamanc-lab/fortune-telling-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown reports or concise answers with tables, calculation steps, and layout recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update MEMORY.md with birth year, sex, derived feng shui classifications, and optional residence details.]

## Skill Version(s):

1.0.0 (source: release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
