## Description:

Downsamples, resizes, compresses, converts, and adjusts DPI for images through Volcengine LAS, supporting JPEG, PNG, and TIFF inputs up to 100 MB and 225 megapixels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and image-processing operators use this skill to prepare Volcengine LAS requests for image downsampling, compression, format conversion, DPI adjustment, thumbnail generation, and batch resizing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script can automatically install an unverified remote SDK wheel and source virtual environments outside the skill directory.

Mitigation: Review the skill before installation, prefer a release that pins and verifies the SDK wheel, and avoid running the environment initializer where untrusted users can create or modify .las_venv.

Risk: The workflow requires LAS and Volcengine credentials and sends images to cloud processing.

Mitigation: Use scoped, revocable credentials and process sensitive images only when cloud processing is permitted for the data.

## Reference(s):

- [las_image_resample API Reference](references/api.md)
- [Pricing Information](references/prices.md)
- [Volcengine LAS Pricing](https://www.volcengine.com/docs/6492/1544808)
- [ClawHub Skill Release](https://clawhub.ai/volcengine-skills/skills/byted-las-image-resample)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include LAS request templates, command sequences, price estimates, and result summaries with billing disclaimers.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
