## Description: <br>
Generates, edits, and analyzes images using Alibaba Cloud DashScope API with supported Qwen and Wanx models via predefined scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to generate images from prompts, edit local or URL-sourced images, create Wanx reference-based outputs, and answer questions about image content through Alibaba Cloud DashScope models. <br>

### Deployment Geography for Use: <br>
Global; the bundled scripts default to Alibaba Cloud DashScope's Beijing endpoint and note Singapore and Virginia endpoints for compatible regional configuration. <br>

## Known Risks and Mitigations: <br>
Risk: First use can change the user's Alibaba Cloud and CLI setup by creating, storing, recycling, or deleting DashScope API keys and by installing the ModelStudio CLI plugin. <br>
Mitigation: Use a dedicated least-privilege RAM user or a manually supplied DASHSCOPE_API_KEY, and review Alibaba Cloud CLI plugin and key changes before running the skill. <br>
Risk: Image prompts and supplied images are processed by Alibaba Cloud DashScope in the configured region. <br>
Mitigation: Avoid submitting confidential images or prompts unless Alibaba Cloud processing in that region is acceptable for the intended use. <br>
Risk: Credential material could be exposed through task output if API keys are manually handled outside the bundled scripts. <br>
Mitigation: Let the provided scripts retrieve keys automatically, do not print or hardcode sk- values, and scan generated output for key-like strings before sharing results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-bailian-image-creator) <br>
- [DashScope API Documentation](references/api-docs.md) <br>
- [DashScope Error Code Reference](references/error-codes.md) <br>
- [DashScope Model List](references/models.md) <br>
- [Professional Prompt Design Guide](references/prompt-guide.md) <br>
- [RAM Policies for Bailian Image Creator](references/ram-policies.md) <br>
- [Alibaba Cloud Model Studio API key documentation](https://help.aliyun.com/zh/model-studio/get-api-key) <br>
- [Alibaba Cloud Model Studio developer reference](https://help.aliyun.com/zh/model-studio/developer-reference) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated image URLs or downloaded image files, and image-analysis text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts validate API responses before reporting success; text-to-image can download generated images locally, while image editing and Wanx generation print generated image URLs.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
