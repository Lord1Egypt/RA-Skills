## Description:

Helps agents search Bilibili, inspect video metadata, fetch comments or danmaku, and prepare or run yt-dlp-based video download workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[epantrip](https://clawhub.ai/user/epantrip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to search for Bilibili videos, inspect metadata, generate download commands, and manage single or batch downloads through yt-dlp-based scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports exploitable script inputs.

Mitigation: Audit and fix argument handling before installation; pass user input as data and test only in a low-privilege sandbox.

Risk: The artifact includes guidance for administrator, sudo, or broad writable-directory execution.

Mitigation: Avoid elevated execution and broad write grants; prefer user-run commands in a dedicated low-privilege workspace.

Risk: Cookie-based downloads may expose real Bilibili session cookies if stored in the skill directory.

Mitigation: Do not store real cookies in the skill directory; keep credentials outside the artifact and provide them only through user-controlled, temporary paths.

Risk: Dependency installation is not pinned.

Mitigation: Make dependency versions explicit and review Python, yt-dlp, and ffmpeg sources before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/epantrip/skills/bilibili-video-downloader)
- [Artifact README](artifact/README.md)
- [Installation guide](artifact/INSTALL.md)
- [Permissions and safety notes](artifact/PERMISSIONS.md)
- [yt-dlp project](https://github.com/yt-dlp/yt-dlp)
- [yt-dlp usage guide](https://github.com/yt-dlp/yt-dlp#usage)
- [FFmpeg downloads](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and short command-output summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may generate yt-dlp commands and can trigger local downloads when executed with write permissions; restricted or high-quality videos may require user-managed cookies.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact also contains a 1.0.0 changelog and v1.2 script notes)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
