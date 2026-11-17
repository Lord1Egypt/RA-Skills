## Description:

Generates meme images with Chinese text overlays or optional AI-generated images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create simple Chinese-language meme images, either offline by placing top and bottom text on a template or online by requesting an AI-generated image from Pollinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI mode sends prompts to Pollinations, which can expose sensitive prompt content to an external service.

Mitigation: Avoid sensitive prompts in AI mode and use text mode when offline or local-only generation is required.

Risk: The script writes the generated image directly to the requested output path.

Mitigation: Choose output paths deliberately and review paths before execution to avoid overwriting unintended files.

Risk: AI image responses may not match the requested meme content or may return unexpected data.

Mitigation: Review generated images before sharing or using them in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-meme-generator)
- [Pollinations image endpoint](https://image.pollinations.ai/prompt/)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG image files with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text mode can run offline; AI mode sends prompts to Pollinations and writes the generated file to the selected output path.]

## Skill Version(s):

1.2.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
