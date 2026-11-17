## Description:

下载 B 站视频到指定目录。使用 yt-dlp，必须用 -o 参数指定完整路径，否则默认下载到 C 盘。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zitao666](https://clawhub.ai/user/zitao666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to prepare yt-dlp commands for downloading Bilibili videos or collections into a user-specified destination directory. The workflow emphasizes explicitly setting yt-dlp's output path to avoid unintended downloads to the current or system drive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided URLs and destination paths may be unsafe when interpolated into shell commands.

Mitigation: Review commands before execution, use only trusted Bilibili URLs and destination paths, and prefer safe argument handling over shell string interpolation.

Risk: The yt-dlp dependency is not pinned in the release evidence.

Mitigation: Install yt-dlp from a trusted source and prefer a revised release that pins the dependency version.

Risk: Omitting the yt-dlp -o output template can place downloads in an unintended directory.

Mitigation: Always include an explicit -o output template with a complete destination path before running yt-dlp.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zitao666/skills/bili-video-downloader)
- [Publisher profile](https://clawhub.ai/user/zitao666)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash and PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yt-dlp; commands should include an explicit -o output template and a trusted destination path.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
