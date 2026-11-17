## Description:

Guides an agent through using the Gemini web app to generate and download images, then using GeminiWatermarkTool to remove Gemini watermarks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imkingjh999](https://clawhub.ai/user/imkingjh999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to control a logged-in browser session for Gemini image generation, download the generated image, and optionally run a watermark-removal utility before sharing or using the output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs an agent to operate a logged-in Gemini browser session.

Mitigation: Run it only in an intended browser profile and review browser actions before submitting prompts, downloading files, or closing tabs.

Risk: The workflow installs or runs an unpinned third-party watermark-removal executable.

Mitigation: Use a trusted, reviewed binary or pinned release and scan it before execution.

Risk: The artifact includes an optional Feishu sharing example with a hard-coded recipient identifier.

Mitigation: Require an explicit recipient and confirmation before uploading or sharing any generated image.

Risk: Removing watermarks can create rights, attribution, or terms-of-service concerns.

Mitigation: Confirm that the user is permitted to modify and use the generated image before removing or distributing watermark-free output.

## Reference(s):

- [Google Gemini](https://gemini.google.com)
- [GeminiWatermarkTool](https://github.com/allenk/GeminiWatermarkTool)
- [GeminiWatermarkTool Releases](https://github.com/allenk/GeminiWatermarkTool/releases)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with browser tool calls, shell commands, and a Python example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a logged-in Google account browser profile, OpenClaw Browser Tool access, and local image download handling.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
