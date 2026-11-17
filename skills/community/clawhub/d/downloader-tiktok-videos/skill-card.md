## Description:

Automatically downloads the latest video, multiple recent videos, or metadata from a public TikTok account or direct TikTok video URL using yt-dlp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stoxca](https://clawhub.ai/user/stoxca)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to retrieve public TikTok videos, bulk-download recent posts, or collect video metadata for archiving and content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use browser-session cookies or cookies.txt files that act like active account credentials.

Mitigation: Keep cookie files private, avoid sharing or committing them, delete them after use, and prefer isolated environments when authenticated access is required.

Risk: The skill can make network requests to TikTok through yt-dlp and write downloaded content to local storage.

Mitigation: Review targets before execution, choose an explicit output directory, and run downloads in an environment where local file writes and network access are acceptable.

Risk: Bypass, proxy, and geo-bypass guidance can be misused to evade platform restrictions.

Mitigation: Use the skill only for authorized content retrieval and do not apply bypass or proxy options to circumvent access controls or platform terms.

Risk: Installing or updating host tools such as yt-dlp or ffmpeg can modify the runtime environment.

Mitigation: Review installation commands before running them, prefer pinned dependencies, and use a virtual environment or container where practical.

## Reference(s):

- [Advanced Techniques](artifact/advanced.md)
- [ClawHub skill page](https://clawhub.ai/stoxca/skills/downloader-tiktok-videos)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python helper usage, metadata text, JSON metadata files, and downloaded media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yt-dlp; ffmpeg is optional but needed for some audio/video merging workflows.]

## Skill Version(s):

1.0.4 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
