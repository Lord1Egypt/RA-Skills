## Description:

Provides design specifications for six UI design systems to guide custom interface generation and review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fize](https://clawhub.ai/user/fize)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and UI engineers use this skill to generate or review custom interfaces against platform-specific and AI-oriented design systems. It guides specification selection, component implementation, and UI validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial, with some file-reading scope and behavior not fully assessed.

Mitigation: Review the skill's file access needs and generated code before use, and avoid exposing sensitive local files in review inputs.

Risk: Using the provided font guidance can cause generated pages to request fonts from Google Fonts.

Mitigation: Use self-hosted or system fonts when external font requests are not appropriate.

## Reference(s):

- [Apple HIG design specification](references/apple-hig.md)
- [Microsoft Fluent design specification](references/microsoft-fluent.md)
- [Google Material design specification](references/google-material.md)
- [Anthropic Editorial design specification](references/anthropic-editorial.md)
- [OpenAI Modernist design specification](references/openai-modernist.md)
- [ArtCraft Blueprint design specification](references/artcraft-blueprint.md)
- [Component specifications](references/component-specs.md)
- [Interaction guidelines](references/interaction-guidelines.md)
- [UI review checklist](references/checklist.md)
- [ClawHub skill page](https://clawhub.ai/fize/skills/custom-ui-spec)

## Skill Output:

**Output Type(s):** [Code, Markdown, Guidance]

**Output Format:** [UI code or a structured Markdown validation report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content follows the selected design specification and target interface.]

## Skill Version(s):

0.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
