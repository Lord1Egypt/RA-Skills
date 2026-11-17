## Description:

Downloads the latest video, multiple recent videos, or metadata from public TikTok accounts and direct TikTok video URLs using yt-dlp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stoxca](https://clawhub.ai/user/stoxca)

### License/Terms of Use:

OpenClaw KBLICENSE 1.0.0

## Use Case:

External users and developers use this skill to retrieve permitted TikTok videos or metadata from public accounts, direct video URLs, and small account archives. It is intended for content the user owns, is authorized to download, or may archive under applicable law.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or update yt-dlp during use.

Mitigation: Preinstall a pinned yt-dlp version through a controlled process before deployment.

Risk: The skill can write downloaded media, metadata, thumbnails, and archive files to local paths.

Mitigation: Constrain accepted output paths and run it with least-privilege filesystem access.

Risk: Cookie-based access can expose browser sessions or exported cookie files.

Mitigation: Avoid --cookies-from-browser and exported cookie files unless explicitly approved for the environment.

Risk: Downloading third-party TikTok content may violate permissions, platform terms, or applicable law.

Mitigation: Use it only for public TikTok content the user is allowed to download or archive.

## Reference(s):

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Skill page](https://clawhub.ai/stoxca/skills/download-video-tiktok)
- [TikTok metadata reference](metadata.md)
- [OpenClaw advanced techniques](advanced.md)
- [OpenClaw KBLICENSE](KBLICENSE.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON metadata files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local MP4 downloads, info JSON files, thumbnails, archive files, and concise status messages when commands are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
