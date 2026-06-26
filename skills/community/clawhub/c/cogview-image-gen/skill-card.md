## Description: <br>
使用智谱AI的CogView模型生成图片。当用户想要AI生成图片时使用此技能，支持中文提示词自动翻译为英文，支持自定义图片尺寸。在首次使用时需要用户配置智谱API密钥。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzh-q](https://clawhub.ai/user/yzh-q) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate images with Zhipu CogView from natural-language prompts, including Chinese prompts that are translated to English and common size presets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and image-generation requests are sent to the external Zhipu CogView service, and API-key use is required. <br>
Mitigation: Use a revocable Zhipu API key and avoid secrets or sensitive personal or business details in prompts. <br>
Risk: The skill references a generate_image.ps1 helper script that was not included in the artifact. <br>
Mitigation: Review the referenced script before running it and confirm it matches the documented CogView image-generation behavior. <br>


## Reference(s): <br>
- [Zhipu AI Open Platform](https://open.bigmodel.cn/) <br>
- [ClawHub skill page](https://clawhub.ai/yzh-q/cogview-image-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with PowerShell command examples and generated image URL output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports 512x512, 768x768, 1024x1024, 1024x768, and 768x1024 image sizes; generated image URLs are described as expiring after about 24 hours.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
