## Description: <br>
Helps agents prepare Alibaba Cloud Model Studio PixVerse video-generation requests for text-to-video, image-to-video, keyframe-to-video, and multi-image reference workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to select PixVerse model variants, prepare normalized DashScope video-generation requests, and capture request and task evidence for Alibaba Cloud Model Studio workflows. <br>

### Deployment Geography for Use: <br>
China mainland (Beijing) for PixVerse service execution. <br>

## Known Risks and Mitigations: <br>
Risk: DashScope API credentials may be exposed if users place secrets in prompts, media URLs, output files, or shared logs. <br>
Mitigation: Use a scoped DASHSCOPE_API_KEY where possible and avoid storing or sharing generated request and evidence files that contain sensitive prompts or media URLs. <br>
Risk: Prompts and media submitted to Alibaba Cloud PixVerse are handled by a third-party cloud provider. <br>
Mitigation: Submit confidential media only when that provider and region are approved for the intended data. <br>
Risk: The release has a naming mismatch noted by the security summary, which may confuse users about the exact Alibaba Cloud video family being used. <br>
Mitigation: Confirm the selected model string starts with pixverse/pixverse-v5.6 and matches the intended text, image, keyframe, or reference workflow before task submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-pixverse-generation) <br>
- [Skill reference sources](references/sources.md) <br>
- [Alibaba Cloud video generation overview](https://help.aliyun.com/zh/model-studio/use-video-generation) <br>
- [PixVerse text-to-video API reference](https://help.aliyun.com/zh/model-studio/pixverse-text-to-video-api-reference) <br>
- [PixVerse image-to-video API reference](https://help.aliyun.com/zh/model-studio/pixverse-image-to-video-api-reference) <br>
- [PixVerse keyframe-to-video API reference](https://help.aliyun.com/zh/model-studio/pixverse-keyframe-to-video-api-reference) <br>
- [PixVerse reference-to-video API reference](https://help.aliyun.com/zh/model-studio/pixverse-reference-to-video-api-reference) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes normalized request JSON under output/aliyun-pixverse-generation/ and may capture task polling evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
