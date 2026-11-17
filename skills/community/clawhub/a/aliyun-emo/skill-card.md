## Description:

Helps agents generate expressive portrait videos from a person image and speech audio using Alibaba Cloud Model Studio EMO (`emo-v1`) with detected portrait boxes and style control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to prepare Alibaba Cloud Model Studio EMO detection and generation requests for expressive talking-head portrait videos from public image and audio URLs.

### Deployment Geography for Use:

China mainland (Beijing)

## Known Risks and Mitigations:

Risk: Portrait images, speech audio, public media URLs, and generated request artifacts may expose sensitive biometric, voice, or request metadata.

Mitigation: Use only controlled public or provider-accessible URLs, avoid sensitive media unless exposure is understood, and review files under output/aliyun-emo before sharing.

Risk: Alibaba Cloud credentials could be exposed if placed directly in prompts, scripts, or generated files.

Mitigation: Keep DASHSCOPE_API_KEY in normal credential storage or Alibaba Cloud credentials, and do not embed API keys in request artifacts.

Risk: Incorrect or invented face_bbox and ext_bbox values can lead to invalid or poor-quality generation requests.

Mitigation: Run EMO detection first and use the returned face_bbox and ext_bbox values before submitting an emo-v1 generation request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-emo)
- [sources.md](references/sources.md)
- [Alibaba Cloud Model Studio video generation overview](https://help.aliyun.com/zh/model-studio/use-video-generation)
- [Alibaba Cloud Model Studio EMO API reference](https://help.aliyun.com/zh/model-studio/emo-api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with shell commands and generated JSON request files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes normalized request payloads under output/aliyun-emo/ and records style_level, face_bbox, and ext_bbox values for traceability.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
