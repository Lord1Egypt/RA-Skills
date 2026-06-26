## Description: <br>
Generate images with Alibaba Cloud Model Studio Z-Image Turbo (z-image-turbo) via DashScope multimodal-generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate text-to-image outputs with Alibaba Cloud DashScope Z-Image Turbo, configure parameters such as size, seed, and prompt extension, and save generated images and response evidence. <br>

### Deployment Geography for Use: <br>
Global, with endpoint selection for Alibaba Cloud DashScope Beijing or Singapore regions. <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to Alibaba Cloud DashScope for image generation. <br>
Mitigation: Use the skill only when third-party processing by Alibaba Cloud is acceptable, and avoid sensitive prompts. <br>
Risk: DashScope credentials are required for normal use. <br>
Mitigation: Use a dedicated API key when possible and keep DASHSCOPE_API_KEY or credential-file values out of logs and shared artifacts. <br>
Risk: Generated images are downloaded to a local output path that may overwrite an existing file. <br>
Mitigation: Choose an output path where replacement is acceptable or use a fresh output directory for each run. <br>
Risk: A custom base_url can route requests away from the intended provider endpoint. <br>
Mitigation: Keep base_url on official or otherwise trusted DashScope endpoints. <br>


## Reference(s): <br>
- [Z-Image Turbo API Reference](references/api_reference.md) <br>
- [Official Z-Image API Reference](https://help.aliyun.com/zh/model-studio/z-image-api-reference) <br>
- [Alibaba Cloud Z-Image API Reference](https://www.alibabacloud.com/help/zh/model-studio/z-image-api-reference) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files] <br>
**Output Format:** [Markdown guidance with bash examples, JSON request and response shapes, and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a DashScope API key and writes generated image output to a local path.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
