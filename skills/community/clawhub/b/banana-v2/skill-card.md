## Description:

Generate AI images with multiple resolutions and models, smartly split them into 2, 4, 6, or 9 image grids, manage galleries, and support five languages including batch downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiyunnet](https://clawhub.ai/user/xiyunnet)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to run a local web app for AI image generation, image-to-image editing, smart grid splitting, gallery management, and batch download workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local web app exposes powerful server controls on port 2688.

Mitigation: Run it only on a trusted local machine and keep port 2688 inaccessible from other users, browsers, and networks.

Risk: API keys, platform tokens, prompts, reference images, generated images, and local paths may be sensitive.

Mitigation: Avoid using confidential files or paid credentials unless credential storage, logging, and data handling have been reviewed and hardened.

Risk: Unauthenticated admin APIs may allow actions such as deleting works or opening local folders.

Mitigation: Review or harden the admin endpoints before using the app with sensitive local files or shared systems.

Risk: Prompts and image content are sent to external AI or upload services.

Mitigation: Use only content that is appropriate to transmit to the configured external services and review the service terms before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiyunnet/skills/banana-v2)
- [Project homepage](https://banana2.zjhn.com)
- [AceData API key setup](https://share.acedata.cloud/r/1uN88BrUTQ)
- [Chinese documentation](docs/zh/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration steps, and local web app outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces generated images, split image files, thumbnails, gallery records, and ZIP downloads through the local web app.]

## Skill Version(s):

1.1.0 (source: frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
