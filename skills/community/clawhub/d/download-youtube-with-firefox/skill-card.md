## Description:

Downloads YouTube videos at the best available quality using yt-dlp, FFmpeg, and a signed-in Firefox session, with JavaScript challenge solving to help access available formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugvfpdcuwfnh](https://clawhub.ai/user/ugvfpdcuwfnh)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users who want to save a YouTube video on a paired computer can use this skill to download and merge the best available video and audio streams into a local media file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The download uses the signed-in Firefox session on the selected paired computer.

Mitigation: Use a dedicated Firefox download profile and keep cookie contents out of conversation history, screen output, and logs.

Risk: The workflow depends on yt-dlp, FFmpeg, and a JavaScript runtime installed on the download computer.

Mitigation: Install dependencies through trusted package managers or verify downloaded releases, and keep in mind that this review does not cover future dependency releases.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ugvfpdcuwfnh/skills/download-youtube-with-firefox)
- [yt-dlp installation guidance](https://github.com/yt-dlp/yt-dlp/wiki/Installation)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Local video file (MKV by default) with a text completion summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the best available video and audio streams; reports the saved file path and size.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
