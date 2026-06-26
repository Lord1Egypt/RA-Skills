## Description: <br>
Automatically downloads the latest video, multiple recent videos, or metadata from a public TikTok account using yt-dlp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stoxca](https://clawhub.ai/user/stoxca) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to retrieve public TikTok videos or video metadata from an account or direct video URL. It supports single-video downloads, recent-video batches, metadata-only checks, and output-file confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run yt-dlp commands that download media and write files to the local filesystem. <br>
Mitigation: Review target accounts, output directories, and generated commands before execution; use an isolated workspace for downloads. <br>
Risk: The documented install commands can modify the host environment, including system Python packages or ffmpeg installation. <br>
Mitigation: Prefer a virtual environment or container and require explicit approval before installing or updating packages. <br>
Risk: Cookie-based downloads can expose active browser session tokens through browser cookie export or cookies.txt files. <br>
Mitigation: Use cookies only when required, keep cookie files private, never commit or share them, and delete them after use. <br>
Risk: Advanced options include proxies, geo-bypass, custom headers, and authentication that can change privacy, policy, or compliance exposure. <br>
Mitigation: Require explicit user approval before authenticated downloads, proxy use, geo-bypass, or custom request headers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stoxca/downloader-tiktok-videos) <br>
- [Advanced Techniques](advanced.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional Python command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local MP4 media files, metadata JSON, archive files, and file-path confirmations when commands are executed.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
