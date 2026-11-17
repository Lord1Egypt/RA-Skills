## Description:

AI Face Swap - Swap face in video using verging.ai API. Supports local video files, YouTube/Bilibili URLs, local and remote face images. Auto-download, trimming, real-time progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[revisual-ai](https://clawhub.ai/user/revisual-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to run face-swap jobs on short videos through the verging.ai API, including trimming input media, uploading video, submitting a face image, polling job status, and optionally downloading the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected face images, videos, and a verging.ai API key to an external service.

Mitigation: Use it only with media you are allowed to process, keep the API key in VERGING_API_KEY, and do not expose the key in shared logs or public repositories.

Risk: The skill can download media from broad user-provided URLs.

Mitigation: Prefer local files or trusted HTTPS URLs and avoid private or internal URLs.

Risk: Temporary media files are written under /tmp/verging-faceswap.

Mitigation: Clean /tmp/verging-faceswap after each run, especially on shared machines.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/revisual-ai/skills/faceswap)
- [verging.ai](https://verging.ai)
- [verging.ai API Docs](https://verging.ai/docs/api)
- [Face Swap Demo](https://youtu.be/xvlZe4uqvY4)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, API request examples, result URLs, and optional downloaded media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VERGING_API_KEY and local command-line tools: yt-dlp, ffmpeg, ffprobe, and curl.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata; artifact frontmatter lists 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
