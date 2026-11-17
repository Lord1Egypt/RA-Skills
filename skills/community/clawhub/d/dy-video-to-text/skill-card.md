## Description:

Extracts speech-to-text from Douyin (TikTok China) videos, retrieves watermark-free download links, and downloads videos from Douyin share links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hljwwyy123](https://clawhub.ai/user/hljwwyy123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to process Douyin share links, extract video metadata, download local MP4 files, and transcribe Chinese or English speech using Alibaba Cloud ASR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scripts may request arbitrary user-supplied URLs before confirming they are Douyin links.

Mitigation: Use only trusted Douyin share links and run the skill in an isolated environment without access to internal services.

Risk: Text extraction sends the video URL and DASHSCOPE_API_KEY to Alibaba Cloud ASR.

Mitigation: Transcribe only content approved for that service and use a dedicated API key with appropriate quota and rotation controls.

Risk: Video download writes MP4 files to local storage.

Mitigation: Choose a controlled output directory and review downloaded files before sharing or further processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hljwwyy123/skills/dy-video-to-text)
- [Alibaba Cloud Bailian API key setup](https://help.aliyun.com/zh/model-studio/get-api-key)
- [Project homepage listed by package metadata](https://github.com/yzfly/douyin-mcp-server)
- [Issue tracker listed by package metadata](https://github.com/yzfly/douyin-mcp-server/issues)

## Skill Output:

**Output Type(s):** [text, JSON, files, shell commands, configuration, guidance]

**Output Format:** [JSON from scripts with concise Markdown guidance for setup, errors, and batch results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write MP4 files to a user-selected output directory; text extraction requires DASHSCOPE_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release evidence and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
