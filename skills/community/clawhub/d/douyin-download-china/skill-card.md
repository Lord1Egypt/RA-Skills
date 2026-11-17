## Description:

抖音视频下载工具。当用户要求下载抖音（豆包）短视频时使用此 skill。支持短链接（如 v.douyin.com/xxx）和完整视频页面链接，自动解析并下载到本地。下载视频为 720p 带水印版本。

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxdong-max](https://clawhub.ai/user/maxdong-max)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent with Douyin links can ask it to resolve short or full Douyin video URLs, retrieve the mobile video identifier, and download a 720p watermarked MP4 to local disk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write local files using filenames derived from external video metadata.

Mitigation: Validate video IDs, sanitize filenames, refuse overwrites, and confirm the final path before writing to ~/Downloads.

Risk: The skill fetches external Douyin URLs through shell commands.

Mitigation: Use it only when the user explicitly asks the agent to fetch a Douyin link, and review commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maxdong-max/skills/douyin-download-china)
- [Douyin API reference](artifact/douyin_api.md)
- [Douyin download usage guide](artifact/douyin-download使用说明.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write MP4 video files to ~/Downloads when the generated shell commands are executed.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
