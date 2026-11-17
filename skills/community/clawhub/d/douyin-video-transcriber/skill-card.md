## Description:

Transcribes one or more Douyin videos by downloading each video through TikHub, extracting audio with ffmpeg, and running local Whisper transcription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahsbnb](https://clawhub.ai/user/ahsbnb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content analysts use this skill to turn Douyin video links into text transcripts for content review, analysis, or copy extraction. It supports batch inputs and writes a Markdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader can contact unexpected network targets when resolving or retrieving video URLs.

Mitigation: Run only with trusted Douyin URLs, validate resolved destinations before download, and restrict network egress where possible.

Risk: The workflow uses a TikHub token to retrieve video download URLs.

Mitigation: Use a token intended for this workflow, avoid shared or privileged environments, and rotate the token if exposure is suspected.

Risk: Temporary media files may be written in shared temporary locations.

Mitigation: Use private temporary directories, limit downloaded file size, and confirm cleanup behavior before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ahsbnb/skills/douyin-video-transcriber)
- [ffmpeg downloads](https://ffmpeg.org/download.html)
- [TikHub Douyin video API endpoint](https://api.tikhub.io/api/v1/douyin/web/fetch_one_video)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown transcription report with plain-text transcript sections and status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts one or more --url values and an optional --output-file path.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
