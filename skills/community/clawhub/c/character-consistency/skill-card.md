## Description:

Helps agents keep the same character, person, or product recognizable across generated scenes, poses, outfits, and styles by using reference images and identity-anchored prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate image requests that preserve a subject's identity while changing scene, pose, outfit, style, or context. It is suited for recurring characters, people, mascots, products, and reference, expression, or outfit sheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference images can contain personal, confidential, or rights-restricted content.

Mitigation: Use only images the user has rights and consent to process, avoid sensitive photos unless appropriate, and prefer controlled-access links over public URLs.

Risk: Generated outputs may drift from the intended identity across scenes, poses, or multi-image sets.

Mitigation: Review outputs for identity consistency and retry outliers with clearer or additional references.

## Reference(s):

- [Worked recipes](artifact/references/examples.md)
- [ClawHub skill page](https://clawhub.ai/runware/skills/character-consistency)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JSON image-generation request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model selection, reference-image inputs, prompt templates, and retry guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
