## Description:

Douyin video downloader that parses a Douyin share link, downloads the video, and returns video metadata plus the saved local file path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andjie98](https://clawhub.ai/user/andjie98)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to download an authorized Douyin video from a shared URL, retrieve basic video metadata, and get the local file path for downstream handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accepts and follows supplied or extracted URLs, which can trigger outbound network requests outside the user's intended destination.

Mitigation: Run it in an environment with restricted outbound networking and provide only trusted Douyin share links.

Risk: Downloads can consume disk space because file size is not bounded by the skill.

Mitigation: Use storage limits or a sandboxed workspace and monitor the download directory.

Risk: Each run replaces ~/.openclaw/workspace/douyin-downloads/douyin_last.mp4.

Mitigation: Copy any video that must be retained before starting another download.

Risk: Downloaded content may be subject to platform terms or third-party rights.

Mitigation: Use the skill only for videos the user is authorized to download and share.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andjie98/skills/douyin-video)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [Console text with a JSON result object and a local MP4 file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads to ~/.openclaw/workspace/douyin-downloads/douyin_last.mp4 and replaces the previous file at that path on each successful run.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
