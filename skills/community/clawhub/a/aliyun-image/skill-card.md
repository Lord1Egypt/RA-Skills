## Description: <br>
aliyun-image helps agents use Alibaba Cloud DashScope Qwen image models for text-to-image generation, image editing, multi-image fusion, style transfer, and image text translation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[StanleyChanH](https://clawhub.ai/user/StanleyChanH) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to generate images from prompts, edit or combine input images, translate text embedded in images, and call the bundled Python client for Alibaba Cloud DashScope workflows. <br>

### Deployment Geography for Use: <br>
Global; API keys and request endpoints must use the same Alibaba Cloud DashScope region documented by the skill. <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, local image files, and translation settings are sent to Alibaba Cloud DashScope, a paid cloud API. <br>
Mitigation: Use the skill only with approved content, avoid confidential or regulated images unless authorized, monitor billing, and keep DASHSCOPE_API_KEY secret. <br>
Risk: Downloaded image outputs can overwrite local files if an existing path is reused. <br>
Mitigation: Save generated downloads into a dedicated output folder and review the destination path before running download commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/StanleyChanH/aliyun-image) <br>
- [Declared ClawHub listing](https://clawhub.com/skill/aliyun-image) <br>
- [Declared repository link](https://github.com/StanleyChanH/aliyun-image-skill) <br>
- [Text-to-image reference](references/text-to-image.md) <br>
- [Image editing reference](references/image-edit.md) <br>
- [Image translation reference](references/image-translate.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with Python and shell examples, JSON API payloads, and returned image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return temporary Alibaba Cloud DashScope image URLs; generated image URLs are documented as valid for 24 hours.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata, created 2026-02-13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
