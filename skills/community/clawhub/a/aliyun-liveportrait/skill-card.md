## Description:

Use when generating lightweight talking-head portrait videos with Alibaba Cloud Model Studio LivePortrait (`liveportrait`) from a detected portrait image and speech audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to prepare Alibaba Cloud Model Studio LivePortrait detection and generation requests for lightweight presenter-style talking-head videos from public portrait image and speech audio URLs.

### Deployment Geography for Use:

China mainland (Beijing region)

## Known Risks and Mitigations:

Risk: The workflow sends portrait images and voice audio to Alibaba Cloud Model Studio using public HTTP/HTTPS URLs.

Mitigation: Use short-lived public links where possible, avoid embedding long-lived secrets in URLs, and only process media that is appropriate to share with the provider.

Risk: Generated request records can include exact portrait and audio URLs.

Mitigation: Clean up output/aliyun-liveportrait/ when request records contain sensitive media locations or parameters.

## Reference(s):

- [Alibaba Cloud Model Studio Video Generation Overview](https://help.aliyun.com/zh/model-studio/use-video-generation)
- [LivePortrait Image Detection API Reference](https://help.aliyun.com/zh/model-studio/liveportrait-detect-api)
- [LivePortrait Video Generation API Reference](https://help.aliyun.com/zh/model-studio/liveportrait-api)
- [LivePortrait Quick Start](https://help.aliyun.com/zh/model-studio/liveportrait-quick-start/)
- [ClawHub Skill Page](https://clawhub.ai/cinience/skills/aliyun-liveportrait)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON request payload files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes normalized request payloads to output/aliyun-liveportrait/ by default.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
