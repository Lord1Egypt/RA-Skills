## Description:

Generate images, video, speech and music, transcribe audio/video files and YouTube, TikTok, X, Twitch or Kick links, describe videos, read text from images (OCR), remove backgrounds and upscale images and video with deAPI. Use when the user asks for any of these, or for a transcript or summary of a video link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deapi-ai](https://clawhub.ai/user/deapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use deAPI through an agent to generate or edit images, video, speech and music, transcribe or describe audio and video, extract text from images, remove backgrounds, and upscale media. The skill also supports checking models, job status, account balance, and API-key usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected media and prompts are sent to deAPI for processing.

Mitigation: Tell users what content will be sent and avoid submitting sensitive media or prompts.

Risk: An admin-role API key can access API-key enumeration tools.

Mitigation: Use a least-privilege API key and provide admin access only when the requested account or key-management task requires it.

## Reference(s):

- [deAPI](https://deapi.ai)
- [deAPI MCP server](https://mcp.deapi.ai/mcp)
- [deAPI API key settings](https://app.deapi.ai/settings/api-keys)
- [deAPI ClawHub release](https://clawhub.ai/deapi-ai/skills/deapi)

## Skill Output:

**Output Type(s):** [Text, Images, Video, Audio, File links]

**Output Format:** [Text results and links to generated media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Long-running jobs may return a request ID for status checks.]

## Skill Version(s):

0.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
