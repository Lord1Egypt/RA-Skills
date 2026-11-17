## Description:

A design-language assistant for Ant Design (antd) that helps agents teach, apply, critique, compare, and theme enterprise UIs using Ant Design values, principles, visual specs, v5 tokens, and design-science rationale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junwugit](https://clawhub.ai/user/junwugit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and agents use this skill to answer Ant Design design-language questions, review UIs, generate or adjust Ant Design themes, and compare antd choices with other design systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be invoked for generic UI critique or design-system requests even when the user did not intend to apply Ant Design.

Mitigation: Ask whether Ant Design guidance should govern the answer when the user is working across multiple design systems or has not named antd.

Risk: Theme examples and design recommendations may not fit a product's accessibility, brand, or implementation constraints without review.

Mitigation: Review generated themes and UI critiques against project accessibility requirements, brand standards, and the target Ant Design version before adoption.

## Reference(s):

- [Skill release page](https://clawhub.ai/junwugit/skills/antd-design-language)
- [Ant Design design spec](https://ant.design/docs/spec)
- [Ant Design - Values & Principles](references/design-values-principles.md)
- [Ant Design - Visual Language](references/visual-language.md)
- [Ant Design v5 - Design Tokens & Theming](references/design-tokens.md)
- [Design-Science & Psychology Behind the Rules](references/psychology-design-science.md)
- [Ant Design vs Other Design Languages](references/comparison.md)
- [Ant Design UI Review Checklist](assets/review-checklist.md)
- [Ant Design v5 Theme Example](assets/theme.example.ts)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown prose with TypeScript and TSX code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include UI critique findings in issue -> principle -> psychological cost -> fix format.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
