## Description:

AI Face Swap - Swap face in video using verging.ai API. Supports local video files, YouTube/Bilibili URLs, local and remote face images. Auto-download, trimming, real-time progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alouhaou](https://clawhub.ai/user/alouhaou)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run face-swap jobs on short videos through the verging.ai API using local media files, video URLs, and face images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos and face images are uploaded to verging.ai for processing.

Mitigation: Use only media you are authorized to process, avoid sensitive media, and proceed only when external upload to verging.ai is acceptable.

Risk: The skill uses shell-based media handling for URLs, files, trimming, and downloads.

Mitigation: Prefer trusted URLs and local files, validate numeric options, avoid shell interpolation, and pin the installer or source where possible.

Risk: Shared temp paths can expose or overwrite media between runs.

Mitigation: Run through a wrapper or implementation that creates a unique private temp directory per run and cleans up media after use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alouhaou/skills/face-swap)
- [Verging API Docs](https://verging.ai/docs/api)
- [Verging Website](https://verging.ai)
- [Face Swap Demo Video](https://youtu.be/xvlZe4uqvY4)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance, Files]

**Output Format:** [Markdown with inline shell commands, API request examples, result URLs, and optional downloaded video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VERGING_API_KEY plus local yt-dlp, ffmpeg, ffprobe, and curl; generated media is limited to 30 seconds per job.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
