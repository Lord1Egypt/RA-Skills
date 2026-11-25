## Description:

用于抖音文案提取、抖音文案一键提取、抖音视频文案提取、抖音视频转文字、抖音口播转文字和抖音逐字稿。用户粘贴抖音视频链接、分享文案或 aweme_id 后，提取视频上下文、原视频简介和口播逐字稿，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users provide a Douyin video link, share text, or aweme_id to obtain video context, the original description, and a spoken transcript. They can also check an existing transcript job or request an SRT subtitle file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs use of a changing, unpinned CLI release while user credentials may be available.

Mitigation: Use a reviewed fixed CLI version and verify its installation integrity before running it with credentials.

Risk: The security review is incomplete because some referenced local paths were not included in the scan.

Mitigation: Review the referenced files before relying on the skill.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files]

**Output Format:** [Structured Markdown, CLI commands, and an optional SRT subtitle file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript results include video context, the original description, spoken transcript, copyable and concise versions, and job status; an SRT file is produced only when requested and valid time segments are returned.]

## Skill Version(s):

0.1.15 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
