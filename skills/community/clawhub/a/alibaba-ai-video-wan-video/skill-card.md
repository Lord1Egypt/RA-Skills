## Description: <br>
Alibaba Cloud Wanx Video Generation - Text to Video, Image to Video, Video Editing <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[powersyang](https://clawhub.ai/user/powersyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to call Alibaba Cloud Wanx video-generation services for text-to-video workflows, with documented options for model, duration, resolution, output file, and negative prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes an embedded Alibaba DashScope API key and can fall back to it when DASHSCOPE_API_KEY is not set. <br>
Mitigation: Remove the embedded key before use, require users to provide their own DASHSCOPE_API_KEY, and rotate any exposed credential. <br>
Risk: Prompts and generation job data are sent to Alibaba Cloud under the configured account. <br>
Mitigation: Avoid submitting sensitive prompts or source media unless the account's billing, retention, and data-handling policies are acceptable for the intended use. <br>
Risk: The documentation advertises image-to-video and digital-human helper scripts that are not present in the artifact. <br>
Mitigation: Validate available scripts before publishing or limit usage guidance to the included text-to-video scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/powersyang/alibaba-ai-video-wan-video) <br>
- [Publisher profile](https://clawhub.ai/user/powersyang) <br>
- [Alibaba Cloud Wanx video generation documentation](https://help.aliyun.com/zh/model-studio/video-generation) <br>
- [Alibaba Cloud text-to-video API reference](https://help.aliyun.com/zh/model-studio/text-to-video-api-reference) <br>
- [Alibaba Cloud text-to-video prompt guide](https://help.aliyun.com/zh/model-studio/text-to-video-prompt) <br>
- [Alibaba Cloud Bailian console](https://bailian.console.aliyun.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; scripts produce MP4 video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY and an enabled Alibaba Cloud DashScope video-generation service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
