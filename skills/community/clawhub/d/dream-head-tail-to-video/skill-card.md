## Description:

Generates four-second videos from text prompts and first and last frame images using the Head Tail to Video (Wan2.1) API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hy-1990](https://clawhub.ai/user/hy-1990)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure and call a third-party DreamAPI/NewportAI video-generation workflow that turns a prompt plus first and last frame images into a short generated video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and first/last-frame image URLs or uploaded media are sent to NewportAI/DreamAPI endpoints.

Mitigation: Avoid confidential, private, or regulated images unless the provider's privacy and retention terms have been reviewed.

Risk: The skill requires storing DREAMHEADTAILTOVIDEO_API_KEY in OpenClaw configuration.

Mitigation: Store the key only in the intended OpenClaw config, rotate it if exposed, and limit access to users who need the integration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hy-1990/skills/dream-head-tail-to-video)
- [DreamAPI get started](https://api.newportai.com/api-reference/get-started)
- [Head Tail to Video Wan2.1 API reference](https://api.newportai.com/api-reference/head-tail-to-video-wan2-1)
- [Dreamface tools](https://tools.dreamfaceapp.com/home)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline shell commands and API endpoint guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DREAMHEADTAILTOVIDEO_API_KEY; inputs include prompt, firstImage, lastImage, and optional resolution.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
