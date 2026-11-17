## Description:

Root entry skill for ChaoJi AI capabilities that routes requests to scene skills for virtual try-on, image cutout, image-to-image generation, or direct ChaoJi API command execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matabear-wyx](https://clawhub.ai/user/matabear-wyx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill pack to route natural-language requests to ChaoJi API workflows for clothing try-on, quick try-on previews, shoe try-on, image-to-image generation, cutout/segmentation, and balance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images and prompts are sent to the ChaoJi API provider for processing.

Mitigation: Use the skill only when the user trusts the provider and is comfortable sharing the selected image inputs with that service.

Risk: The skill requires ChaoJi AK/SK credentials.

Mitigation: Use narrowly scoped credentials, prefer environment variables or a protected secret manager, and restrict permissions on any credentials file.

Risk: Local file inputs and downloaded outputs may be broader than the documented permission boundaries.

Mitigation: Avoid arbitrary local paths as image inputs until workspace allowlisting and image validation are enforced.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/matabear-wyx/skills/chaoji-skills)
- [Credentials Guide](references/credentials-guide.md)
- [ChaoJi API Documentation](https://doc.metac-inc.com/marketing/open-api.html)
- [Chaoji Tryon Workflow](skills/chaoji-tryon/references/workflow.md)
- [Chaoji Tryon Fast Workflow](skills/chaoji-tryon-fast/references/workflow.md)
- [Chaoji Tryon Shoes Workflow](skills/chaoji-tryon-shoes/references/workflow.md)
- [Chaoji Img2img Workflow](skills/chaoji-img2img/references/workflow.md)
- [Chaoji Cutout Workflow](skills/chaoji-cutout/references/workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [JSON responses with media URLs, local output paths, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include task IDs, generated image URLs, downloaded image paths, and user-facing error guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
