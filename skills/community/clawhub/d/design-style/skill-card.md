## Description:

Design Style helps agents select and apply a design-system prompt library when building or improving frontend interfaces, web pages, UI components, and visual styling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benangel65](https://clawhub.ai/user/benangel65)

### License/Terms of Use:


## Use Case:

Developers and design-focused coding agents use this skill to choose a frontend aesthetic, load the matching style prompt, and produce style-consistent UI code, configuration, and guidance for web interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated frontend code may include external fonts, remote texture URLs, or animation libraries suggested by the style prompts.

Mitigation: Review generated code before deployment and replace external assets with local or approved resources for privacy-sensitive sites.

Risk: Some style prompts may encourage forced dark or light themes, uppercase text, or motion-heavy effects that can reduce accessibility or fit poorly with an existing product.

Mitigation: Check contrast, typography, motion, and theme behavior against project accessibility and brand requirements before release.

## Reference(s):

- [Design Style Skill Reference Guide](artifact/reference.md)
- [Style Mapping](artifact/styles-mapping.json)
- [Design Style Prompt Library](artifact/prompts/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional code, shell, and configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the selected design style and the user's frontend stack.]

## Skill Version(s):

1.0.0 (source: target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
