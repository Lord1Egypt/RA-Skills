## Description:

下载抖音视频到本地（无水印），以mp4格式默认保存在桌面目录。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvleiai123](https://clawhub.ai/user/lvleiai123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to extract a Douyin share URL from user-provided text and download the resolved no-watermark video as an MP4 file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted Douyin links are sent to an undeclared third-party resolver service.

Mitigation: Disclose the resolver service to users and ask for confirmation before sending links externally.

Risk: The script trusts the resolver response when selecting a download URL and saving a file to the Desktop.

Mitigation: Validate returned domains, file size, and content type before downloading, and prompt before writing files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lvleiai123/skills/douyin-no-watermark-downloader)

## Skill Output:

**Output Type(s):** [text, shell commands, code, files, guidance]

**Output Format:** [Markdown guidance with shell command examples and a downloaded MP4 file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads are saved to the user's Desktop by default with a timestamped .mp4 filename.]

## Skill Version(s):

1.0.9 (source: server release evidence; artifact frontmatter reports 1.0.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
