## Description:

Generate digital human talking avatar videos from images and audio using DreamAvatar 3.0 Fast API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hy-1990](https://clawhub.ai/user/hy-1990)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create talking-avatar videos from a supplied image and audio file or public URLs, with optional prompt and resolution settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected image and audio files to DreamAvatar/NewportAI and temporary OSS storage.

Mitigation: Use only media you have permission to process, and avoid private, biometric, confidential, or third-party media unless the retention and access model is acceptable.

Risk: A DreamAPI key is required for API access.

Mitigation: Store DREAM_API_KEY in the OpenClaw skill environment configuration and avoid exposing it in prompts, logs, or shared files.

Risk: Generated media may depend on externally hosted input URLs and temporary uploaded file URLs.

Mitigation: Use publicly accessible URLs only when intended, and retrieve generated results before the temporary upload URLs expire.

## Reference(s):

- [Dream Avatar ClawHub Skill Page](https://clawhub.ai/hy-1990/skills/dream-avatar)
- [DreamAPI Get Started](https://api.newportai.com/api-reference/get-started)
- [Dreamface AI Tools](https://tools.dreamfaceapp.com/home)
- [DreamAvatar Get Upload Policy API](https://api.newportai.com/api/file/v1/get_policy)
- [DreamAvatar Image to Video 3.0 Fast API](https://api.newportai.com/api/async/dreamavatar/image_to_video/3.0fast)
- [DreamAvatar Async Result API](https://api.newportai.com/api/getAsyncResult)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, text]

**Output Format:** [Markdown with inline shell commands, JSON examples, API request details, and generated video URL guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses DREAM_API_KEY; accepts local image/audio files or public URLs; returns asynchronous task status and final MP4 video URL when complete.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
