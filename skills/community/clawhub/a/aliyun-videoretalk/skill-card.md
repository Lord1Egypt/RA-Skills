## Description: <br>
Use when replacing lip sync in existing videos with Alibaba Cloud Model Studio VideoRetalk (`videoretalk`) for dubbed videos, replaced narration, or synchronized talking-head videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media automation teams use this skill to prepare Alibaba Cloud Model Studio VideoRetalk requests for replacing a person video's lip sync with a new speech track. It supports public video and audio URLs, optional target-face selection, and video-extension settings for asynchronous VideoRetalk jobs. <br>

### Deployment Geography for Use: <br>
China mainland (Beijing) <br>

## Known Risks and Mitigations: <br>
Risk: Selected video and audio URLs are sent to Alibaba Cloud for processing. <br>
Mitigation: Use only media that is approved for Alibaba Cloud processing, avoid secret-bearing or long-lived signed URLs, and confirm the required region and account controls before submitting jobs. <br>
Risk: The helper stores full request details locally, including media URLs and task snapshots. <br>
Mitigation: Keep generated output files private, store them only in approved locations, and delete them after use when they are no longer needed. <br>
Risk: Multi-face videos can target the wrong person if face selection is ambiguous. <br>
Mitigation: Provide a reference image URL for multi-face inputs and review generated outputs before publishing or downstream use. <br>


## Reference(s): <br>
- [Aliyun Videoretalk release page](https://clawhub.ai/cinience/aliyun-videoretalk) <br>
- [Publisher profile](https://clawhub.ai/user/cinience) <br>
- [Video generation overview](https://help.aliyun.com/zh/model-studio/use-video-generation) <br>
- [VideoRetalk product documentation](https://help.aliyun.com/zh/model-studio/videoretalk/) <br>
- [VideoRetalk API reference](https://help.aliyun.com/zh/model-studio/videoretalk-api) <br>
- [Artifact reference sources](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes normalized request JSON and records input URLs, face-selection settings, video-extension choice, and polling snapshots under output/aliyun-videoretalk/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
