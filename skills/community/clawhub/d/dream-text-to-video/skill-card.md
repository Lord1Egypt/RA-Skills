## Description:

Generate videos from text using the Text to Video (Wan2.1) API, producing 4-second videos from text descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hy-1990](https://clawhub.ai/user/hy-1990)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure DreamAPI credentials and generate short text-to-video outputs from prompts through NewportAI/DreamAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and generation requests are sent to NewportAI/DreamAPI, and those prompts may contain sensitive or personal information.

Mitigation: Avoid submitting secrets, private personal data, or confidential material unless the user accepts the provider's handling of that data.

Risk: The skill requires storing a DreamAPI key in OpenClaw configuration.

Mitigation: Use a scoped API key where possible, keep it out of prompts and logs, and rotate it if it may have been exposed.

## Reference(s):

- [Dream Text to Video skill page](https://clawhub.ai/hy-1990/skills/dream-text-to-video)
- [DreamAPI get started](https://api.newportai.com/api-reference/get-started)
- [Text to Video Wan2.1 API reference](https://api.newportai.com/api-reference/text-to-video-wan2-1)
- [Dreamface AI tools](https://tools.dreamfaceapp.com/home)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with inline bash commands, API endpoint references, and parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DREAMTEXTTOVIDEO_API_KEY; prompt max is 1500 characters; supported resolutions are 480p and 720p; generated videos are described as 4 seconds long.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
