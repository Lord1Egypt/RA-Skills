## Description:

Creates short video highlight clips with burned-in subtitles and an AI-generated cover from YouTube URLs or local video inputs using yt-dlp, MiniMax, and ffmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freak30](https://clawhub.ai/user/freak30)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-automation users can use this skill to extract short highlight clips from long-form YouTube videos, podcasts, lectures, livestream replays, or local videos. It is intended to produce social-video-ready clips with subtitles and a generated cover image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports a live-looking MiniMax API key in the skill materials.

Mitigation: Install only after the MiniMax key has been revoked and removed from the skill documentation and any distributed files.

Risk: The release evidence reports that subtitle handling can send the wrong local subtitle file to an external AI service.

Mitigation: Use a per-run working directory or exact downloaded subtitle path, and avoid shared output folders containing private SRT files.

Risk: The release evidence states that video subtitles processed by this skill may be sent to MiniMax.

Mitigation: Treat subtitles as third-party API data and avoid processing private, confidential, or restricted transcripts unless that transfer is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freak30/skills/clipping-video-highlights)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Command-line execution that writes MP4 clips, a cover image, and terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs cover.jpg and clip_XX.mp4 files in the requested output directory.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
