## Description:

一个用于从Bilibili视频URL中检索字幕、弹幕和评论信息的MCP服务器。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retrieve subtitles, danmaku, and popular comments from Bilibili video URLs through the Xiaobenyang MCP API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill saves a Xiaobenyang API key in a local plaintext .env file.

Mitigation: Use a low-privilege, non-reusable API key, confirm .env is excluded from source control, and restrict local file access before use.

Risk: Leftover Gaokao/template references make the backend service and credential scope unclear.

Mitigation: Review the skill before installation and require the publisher to clarify the backend and credential scope before trusted use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/bilibili-video-info)
- [Xiaobenyang API key site](https://xiaobenyang.com)
- [Bilibili video URL example](https://www.bilibili.com/video/BV1x341177NN)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown summary of API JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Bilibili video URL and a Xiaobenyang API key; supported result categories are subtitles, danmaku, and popular comments.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
