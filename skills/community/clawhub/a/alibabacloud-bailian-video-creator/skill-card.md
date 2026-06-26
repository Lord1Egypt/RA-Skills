## Description: <br>
Alibabacloud Bailian Video Creator helps agents generate, edit, and analyze videos through Alibaba Cloud DashScope models for text-to-video, image-to-video, reference-to-video, video editing, and video understanding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to route video creation, video editing, and video understanding requests to the appropriate Alibaba Cloud DashScope workflow. It is suited for generating short videos from text, images, or references, repainting or region-editing existing videos, and producing video-content analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send prompts and media URLs to Alibaba Cloud DashScope and may incur billing. <br>
Mitigation: Install only when cloud processing and billing are acceptable, and review prompts and media URLs before execution. <br>
Risk: The skill can automatically create persistent Alibaba Cloud API keys and install the Alibaba Cloud CLI ModelStudio plugin during normal use. <br>
Mitigation: Prefer a manually created, limited DASHSCOPE_API_KEY and install the ModelStudio plugin yourself before use. <br>
Risk: Broad Alibaba Cloud account permissions can allow API key creation and deletion beyond what is needed for simple video generation. <br>
Mitigation: Avoid broad account permissions unless automatic API-key lifecycle management is explicitly required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-bailian-video-creator) <br>
- [Publisher profile](https://clawhub.ai/user/sdk-team) <br>
- [API documentation](references/api-docs.md) <br>
- [Model list](references/models.md) <br>
- [Prompt guide](references/prompt-guide.md) <br>
- [Error codes](references/error-codes.md) <br>
- [RAM policies](references/ram-policies.md) <br>
- [Alibaba Cloud text-to-video API reference](https://help.aliyun.com/zh/model-studio/text-to-video-api-reference) <br>
- [Alibaba Cloud image-to-video API reference](https://help.aliyun.com/zh/model-studio/image-to-video-api-reference) <br>
- [Alibaba Cloud Wanx VACE API reference](https://help.aliyun.com/zh/model-studio/wanx-vace-api-reference) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal output that may include generated video URLs, analysis text, script invocations, configuration steps, and error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generation and editing tasks are asynchronous and require polling until completion; successful remote video tasks may incur Alibaba Cloud billing.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
