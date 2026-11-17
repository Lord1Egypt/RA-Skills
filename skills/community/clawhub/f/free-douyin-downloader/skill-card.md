## Description:

下载抖音视频到本地文件，支持抖音短链、包含短链的分享文本，以及 douyin.com/video/... 视频直链输入。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wudi](https://clawhub.ai/user/wudi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent in downloading supported Douyin videos locally, including links pasted from Douyin share text. It is intended for saving video files when the user already has a Douyin short link or direct video URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weak URL validation can cause the script to contact non-Douyin or internal URLs.

Mitigation: Use only trusted Douyin links or share text and avoid passing arbitrary short links or untrusted pasted content.

Risk: Downloads have no size limit and may consume unexpected disk space.

Mitigation: Save output to a dedicated download folder with enough free space and review the download before broader use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local execution of a Python standard-library script that makes outbound web requests and writes MP4 files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
