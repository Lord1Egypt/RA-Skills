## Description:

DesignKit Ecommerce AI Studio helps agents route DesignKit workflows for background removal, image restoration, ecommerce listing-image generation, and A+ detail-page planning and rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meituskills](https://clawhub.ai/user/meituskills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run Chinese-language DesignKit image-editing and ecommerce image-production workflows through an agent. It supports single-image edits, product listing image sets, and A+ detail-page planning and rendering from user-provided image URLs or local image paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configurable network endpoints can receive the API key and uploaded images.

Mitigation: Keep custom API-base environment variables unset unless you control and trust the endpoint.

Risk: Local image paths may be uploaded to DesignKit/OpenClaw for processing.

Mitigation: Provide only local image paths intended for upload, and tell users before sending local files to the remote service.

Risk: Unpinned direct installation commands may bypass the ClawHub review path.

Mitigation: Prefer the ClawHub inspect/install path before installing or running the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/meituskills/skills/designkit-skills)
- [DesignKit OpenClaw](https://www.designkit.cn/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown and structured text describing generated image URLs, local saved paths, workflow status, and user-facing guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download generated ecommerce or A+ detail images to a local output directory; requires DESIGNKIT_OPENCLAW_AK.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
