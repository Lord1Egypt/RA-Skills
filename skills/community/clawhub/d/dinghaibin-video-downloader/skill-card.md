## Description:

Download videos from YouTube and other video platforms. Use when user needs to download videos for offline viewing, extract audio from videos, or save video metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to download online videos, extract audio, inspect available formats, and save video metadata for offline workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can install an unpinned third-party yt-dlp package at runtime.

Mitigation: Review the skill before installation and use a reviewed, pinned yt-dlp version in an isolated environment.

Risk: The skill fetches remote media and writes video, audio, or metadata files locally.

Mitigation: Run it with an explicit output path in an isolated workspace and review resulting files before reuse.

Risk: Downloaded content may be subject to platform terms or third-party rights.

Mitigation: Confirm permission to download and use the requested content before running the downloader.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and local file outputs from the downloader script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch remote media through yt-dlp and write video, audio, or metadata files to the local filesystem.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
