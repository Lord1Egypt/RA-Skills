## Description:

Explanation Docs helps agents write understanding-oriented explanation documentation, including conceptual guides, design rationale, and architecture explanations that clarify why systems work the way they do.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, architects, and documentation maintainers use this skill to draft or revise explanation documents that build reader understanding of concepts, design decisions, trade-offs, and architecture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad how/why writing requests where explanation is not the right documentation type.

Mitigation: Classify the draft against the explanation, tutorial, how-to, and reference distinctions before applying the explanation template.

Risk: The skill references separate docs-style guidance that is not bundled in the inspected artifact.

Mitigation: Treat related style links as supplemental references and verify that guidance is available and appropriate before relying on it.

## Reference(s):

- [docs-style skill](../docs-style/SKILL.md)
- [Diataxis compass](../docs-style/references/diataxis-compass.md)
- [howto-docs skill](../howto-docs/SKILL.md)
- [reference-docs skill](../reference-docs/SKILL.md)
- [tutorial-docs skill](../tutorial-docs/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown prose, templates, checklists, and editing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance-only skill; the inspected artifact does not execute code or access user data.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
