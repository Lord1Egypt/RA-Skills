## Description:

Scrapes YouTube Shorts hooks from a creator channel, trims them, and stitches them with a CTA video to produce ready-to-post vertical content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jean-maradiaga](https://clawhub.ai/user/jean-maradiaga)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and content operators use this skill to generate short-form vertical videos by combining hooks from YouTube Shorts creators with their own CTA video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run external pipeline code with local file access and optional YouTube API-key access.

Mitigation: Use only a trusted, pinned, inspected pipeline source, run it in a restricted working directory, and avoid passing secrets unless they are necessary.

Risk: Generated videos may include downloaded or stitched content that the user does not have rights to publish.

Mitigation: Confirm rights to the source Shorts, CTA video, and final stitched outputs before publishing.

## Reference(s):

- [AI Hookbot on ClawHub](https://clawhub.ai/jean-maradiaga/skills/ai-hookbot)
- [OpenClaw](https://openclaw.ai)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)
- [Google Cloud Console](https://console.cloud.google.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration values, generated file paths, and run summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports hook counts, created video counts, output directory, and sanitized failures.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
