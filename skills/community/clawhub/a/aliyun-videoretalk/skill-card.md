## Description:

Use when replacing lip sync in existing videos with Alibaba Cloud Model Studio VideoRetalk (`videoretalk`). Use when creating dubbed videos, replacing narration, or synchronizing a talking-head video to a new speech track.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media automation teams use this skill to prepare Alibaba Cloud Model Studio VideoRetalk requests for replacing lip sync in person videos with a new speech track. It supports dubbed videos, narration replacement, multi-face targeting with a reference image, and optional video extension for longer audio.

### Deployment Geography for Use:

China mainland (Beijing)

## Known Risks and Mitigations:

Risk: Input video and audio URLs are sent to Alibaba Cloud DashScope and the exact URLs may be stored locally under output/aliyun-videoretalk.

Mitigation: Use only approved public media URLs, avoid sensitive links, and clean the output directory after work that includes sensitive media references.

Risk: The workflow requires a DashScope API key for provider access.

Mitigation: Use a scoped DashScope API key where possible and keep credentials in environment variables or the documented Alibaba Cloud credentials file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-videoretalk)
- [Alibaba Cloud video generation overview](https://help.aliyun.com/zh/model-studio/use-video-generation)
- [VideoRetalk product documentation](https://help.aliyun.com/zh/model-studio/videoretalk/)
- [VideoRetalk API reference](https://help.aliyun.com/zh/model-studio/videoretalk-api)
- [Source references](references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON files]

**Output Format:** [Markdown guidance with shell commands and normalized JSON request payloads written to files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes request payloads, face selection settings, and task polling snapshots under output/aliyun-videoretalk; records exact input media URLs and video_extension settings.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
