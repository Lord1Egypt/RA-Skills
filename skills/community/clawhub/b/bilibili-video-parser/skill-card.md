## Description:

Downloads a single Bilibili video with yt-dlp and passes the local video file to a video-analysis skill for visual understanding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielcy](https://clawhub.ai/user/danielcy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill when an agent needs to download a Bilibili video by URL or BV ID and analyze the downloaded visual content. The workflow checks for yt-dlp, stores videos under the workspace, and delegates analysis to a separate video-analysis skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The download command may be unsafe if BV IDs or Bilibili URLs are accepted without validation.

Mitigation: Validate BV IDs and Bilibili HTTPS URLs, pass arguments without shell interpolation, and add -- before the URL.

Risk: The workflow may install the doubao-video-analyze skill without a verified source.

Mitigation: Require explicit approval or a pinned trusted source before installing doubao-video-analyze.

Risk: The skill downloads Bilibili videos into the workspace.

Mitigation: Use only when workspace video downloads are acceptable for the user's permissions, storage, and data-handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielcy/skills/bilibili-video-parser)
- [yt-dlp project](https://github.com/yt-dlp/yt-dlp)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Markdown, Guidance]

**Output Format:** [Markdown guidance with bash commands, workspace file paths, and delegated analysis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yt-dlp or YT_DLP_PATH and may create MP4 files under ./bilibili/videos.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
