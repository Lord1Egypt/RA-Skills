## Description:

Generates images through fal.ai and BytePlus Seedream APIs for single-image, batch, and reference-guided photo, poster, or visual-asset workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-production agents use this skill to generate photos, posters, and other visual assets from text prompts or reference images using fal.ai or BytePlus Seedream.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, generated images, and reference images may be sent to fal.ai or BytePlus.

Mitigation: Treat those inputs as external API data and avoid sending sensitive or restricted content unless approved for those services.

Risk: The artifact references a generate.py script that is not included in the evidence package.

Mitigation: Review any supplied generate.py script before installation or execution.

Risk: The skill requires FAL_API_KEY and BYTEPLUS_API_KEY credentials.

Mitigation: Use scoped API keys with appropriate usage limits and rotate them according to local credential policy.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/fal-image-gen)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell command examples, environment variable configuration, JSON batch examples, and generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved under output/YYYY-MM-DD/ and emitted through MEDIA lines when the referenced generation script is available.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
