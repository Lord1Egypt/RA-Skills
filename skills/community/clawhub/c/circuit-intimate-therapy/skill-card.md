## Description:

This skill helps agents explain, diagnose, and teach relationship dynamics through circuit analogies such as RLC response, DC bias, impedance, damping, and diode behavior, with optional local HTML demos for interactive explanation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junwugit](https://clawhub.ai/user/junwugit)

### License/Terms of Use:

MIT-0

## Use Case:

Counselors, educators, and relationship-theory learners can use this skill to translate intimate-relationship concepts into circuit-language explanations, structured case readings, intervention planning, and teaching demos. It is a conceptual and educational aid, not a substitute for clinical diagnosis, crisis response, medical advice, or legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive relationship-case details may be written into local HTML files.

Mitigation: Install and use the skill only when users understand the write location, can decline app generation, and can manage or delete generated files.

Risk: The circuit analogy may be mistaken for clinical diagnosis or crisis intervention.

Mitigation: Present outputs as conceptual teaching and planning aids, and route self-harm, family violence, coercion, child abuse, or other urgent safety situations to appropriate local emergency or professional resources.

Risk: Generated relationship guidance could be incomplete or misleading for a specific couple or family context.

Mitigation: Review outputs before relying on them, verify case assumptions with the user, and keep interventions grounded in qualified human judgment.

## Reference(s):

- [Skill Definition](artifact/SKILL.md)
- [Part 1: Basic Component Mapping](artifact/references/components.md)
- [Part 2 and 3: DC Bias and Complex Impedance Vector](artifact/references/dc-and-zvector.md)
- [Part 4: Conjugate Relationships and Damping](artifact/references/conjugate-and-damping.md)
- [Part 5: Diode and Nonlinear Phenomena](artifact/references/diodes.md)
- [Part 6: Relationship Theory Mapping](artifact/references/theory-mapping.md)
- [Part 7: Diagnosis and Intervention](artifact/references/diagnosis-intervention.md)
- [Case Walkthrough](artifact/references/case-walkthrough.md)
- [Visualization App Guide](artifact/references/apps-guide.md)
- [HTML App Generation Template](artifact/references/app-generation-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Markdown explanations with optional single-page HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write context-specific HTML demos under ~/circapps/generated/ when the skill's app-generation behavior is applicable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
