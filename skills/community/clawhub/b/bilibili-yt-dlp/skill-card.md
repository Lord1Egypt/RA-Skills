## Description:

使用 yt-dlp 和 ffmpeg 下载哔哩哔哩视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xbos1314](https://clawhub.ai/user/xbos1314)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to download Bilibili videos from b23.tv or bilibili.com links with yt-dlp, then merge separate audio and video streams with ffmpeg when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing yt-dlp or ffmpeg from untrusted sources can introduce dependency or local execution risk.

Mitigation: Install dependencies from trusted sources and prefer an isolated environment.

Risk: Using --cookies-from-browser or --cookies can expose authenticated Bilibili session data.

Mitigation: Use cookies only when necessary, protect cookie files as credentials, and avoid sharing them.

Risk: Downloaded or shared videos may violate access permissions or copyright restrictions.

Mitigation: Download and share only videos the user is authorized to access and distribute.

## Reference(s):

- [ffmpeg downloads](https://ffmpeg.org/download.html)
- [Bilibili video URL example](https://www.bilibili.com/video/BVxxxx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash, JavaScript, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers local downloads, optional browser cookies, and ffmpeg-based media merging.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
