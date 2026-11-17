## Description:

Helps agents use Agnes AI image and video APIs to generate or edit images and create videos with Agnes-Image-2.0-Flash and Agnes-Video-V2.0.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jefsky](https://clawhub.ai/user/jefsky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to configure Agnes API calls and helper-script commands for image generation, image editing, video generation, image-to-video, and multi-image composition workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and the Agnes API key are sent to a third-party Agnes AI service.

Mitigation: Use the skill only when that data sharing is intended, avoid sensitive prompts or private media unless the service is trusted, and keep the API key in environment variables.

Risk: The helper script downloads generated media locally without download URL, size, timeout, or symlink protections.

Mitigation: Run the helper script without elevated privileges in a private output directory and review downloaded media handling before using it in automated workflows.

## Reference(s):

- [Agnes API Platform](https://platform.agnes-ai.com/)
- [Agnes API v1 Base URL](https://apihub.agnes-ai.com/v1)
- [ClawHub Skill Page](https://clawhub.ai/jefsky/skills/agnes-image-video)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python and shell command examples; the helper script saves generated image or video files locally.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Agnes API key and sends prompts, image URLs, and generation parameters to Agnes AI endpoints.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
