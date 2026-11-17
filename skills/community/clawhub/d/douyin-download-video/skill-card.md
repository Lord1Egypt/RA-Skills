## Description:

Downloads videos from yt-dlp-supported sites using yt-dlp and ffmpeg, with options for quality, audio-only output, and output directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heihu123](https://clawhub.ai/user/heihu123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to download video or audio from yt-dlp-supported sites, including YouTube, Bilibili, Douyin, and other supported services. It is intended for cases where an agent needs to save media files with configurable quality, format, and destination folder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A normal download can automatically install or fetch executable tools without integrity checks or clear per-use consent.

Mitigation: Review before installing, use an environment where automatic package installation is acceptable, and prefer installing reviewed versions of yt-dlp and ffmpeg yourself.

Risk: Browser-cookie options can expose logged-in session credentials to yt-dlp.

Mitigation: Avoid browser-cookie options unless they are necessary and you understand the credential exposure.

Risk: The skill writes downloaded media files to local folders.

Mitigation: Restrict output paths to folders you intend the tool to write to.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/heihu123/skills/douyin-download-video)
- [FFmpeg downloads](https://ffmpeg.org/download.html)
- [Gyan FFmpeg Windows build](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Downloaded video or audio files with terminal progress text and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write media files to the user's Downloads folder or a caller-specified output directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
