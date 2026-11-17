## Description:

Generate videos from images using the Image to Video (Wan2.1) API, producing 4-second videos from text descriptions and images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hy-1990](https://clawhub.ai/user/hy-1990)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to configure an API key and generate short image-to-video outputs from prompts, image URLs, or uploaded local images through DreamAPI/NewportAI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and uploaded local images are sent to the DreamAPI/NewportAI service.

Mitigation: Avoid confidential, personal, or sensitive media unless the provider's privacy and retention terms have been reviewed and accepted.

Risk: The skill requires an API key configured in the agent environment.

Mitigation: Store the DREAMIMAGETOVIDEO_API_KEY value using the agent's configuration mechanism and avoid exposing it in shared prompts, logs, or public files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hy-1990/skills/dream-image-to-video)
- [DreamAPI Get Started](https://api.newportai.com/api-reference/get-started)
- [Image to Video (Wan2.1) API Reference](https://api.newportai.com/api-reference/image-to-video-wan2-1)
- [Dreamface AI Tools](https://tools.dreamfaceapp.com/home)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and API endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides API-key configuration, accepts prompts up to 1500 characters, supports image URLs or uploaded local images, and describes 480p or 720p output options.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
