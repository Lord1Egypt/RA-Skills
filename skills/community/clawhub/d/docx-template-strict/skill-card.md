## Description:

Strictly fills DOCX templates by replacing placeholder tokens while preserving cover pages, headers and footers, sections, styles, fonts, and layout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lpq6](https://clawhub.ai/user/lpq6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, students, and document authors use this skill to fill Word report, paper, or assignment templates with text, figures, captions, and references while preserving the original DOCX layout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trusted-template assumptions: generated files preserve hidden DOCX package content from the source template.

Mitigation: Use templates from trusted sources, review generated documents before sharing them, and do not use this skill as a sanitizer for unknown Word files.

Risk: Template placeholder mismatch can leave required content unfilled or cause generation to fail.

Mitigation: Use continuous placeholder tokens, provide data for every required token, and review the script's unreplaced-token QA output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lpq6/skills/docx-template-strict)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with bash and JSON examples; script execution produces a DOCX file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit placeholder tokens and fails if unreplaced tokens remain or DOCX section counts change.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
