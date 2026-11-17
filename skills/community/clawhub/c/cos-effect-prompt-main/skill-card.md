## Description:

Generates structured JSON preset envelopes for cosplay photo retouching, visual effects, style transfer, and reverse-engineered Nano Banana image-editing prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aleaaaan](https://clawhub.ai/user/aleaaaan)

### License/Terms of Use:

MIT

## Use Case:

External users and creators use this skill to turn Chinese-language cosplay photo-editing requests into importable JSON presets for Nano Banana, including effects, retouching, body shaping, clothing cleanup, lighting, backgrounds, and style presets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create JSON files locally as part of preset generation.

Mitigation: Review generated file paths and file contents before relying on saved presets.

Risk: The style-learning feature can persist user-provided style text into the skill data and influence future preset generation.

Mitigation: Use style learning only with trusted style descriptions and review learned entries before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aleaaaan/skills/cos-effect-prompt-main)
- [Effects reference](references/effects.md)
- [Portrait retouching reference](references/portrait.md)
- [Fallback module reference](references/fallback.md)
- [MJ style reference](references/mj-style.md)
- [Nano Banana editing reference](references/nano-banana.md)
- [Preset envelope example](references/preset-envelope.json)
- [Instruction JSON template](references/template.json)

## Skill Output:

**Output Type(s):** [text, json, configuration, guidance]

**Output Format:** [Markdown containing an importable JSON preset envelope; the preset content is an escaped instruction JSON string.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preset envelopes include id, title, content, category, subCategory, refImages, _isFactory, and numeric slider parameters for intensity, style weight, and light blending.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
