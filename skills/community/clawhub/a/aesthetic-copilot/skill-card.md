## Description:

Use when the user wants to generate high-fidelity PROMPTS for Text-to-Image models (Flux, Ideogram, Midjourney) based on vague layout/content descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchen913](https://clawhub.ai/user/chenchen913)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creative teams use this skill to turn vague visual ideas into structured, commercial-grade text-to-image prompts for Flux, Ideogram, and Midjourney. It classifies intent, selects an aesthetic style and layout, applies visual modifiers, and returns a ready-to-use prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated image prompts may include aesthetic, layout, or model-specific wording that is unsuitable for a particular brand, campaign, or downstream image model.

Mitigation: Review generated prompts and resulting images before publication or commercial use.

Risk: The skill depends on bundled markdown style and template files, so missing or modified files can degrade prompt quality or routing accuracy.

Mitigation: Install the complete release artifact and verify the bundled files are present before using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenchen913/skills/aesthetic-copilot)
- [Publisher profile](https://clawhub.ai/user/chenchen913)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-wrapped plaintext prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single text-to-image prompt with template, style DNA, layout, concept, and filled prompt content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
