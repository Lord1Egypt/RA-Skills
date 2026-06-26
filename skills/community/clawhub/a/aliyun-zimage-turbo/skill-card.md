## Description: <br>
Generates text-to-image outputs with Alibaba Cloud Model Studio Z-Image Turbo via the DashScope multimodal-generation API, including controls for size, seed, prompt extension, and request/response mapping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate images through Alibaba Cloud DashScope Z-Image Turbo, configure prompts and generation parameters, and save normalized response evidence and downloaded image files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script can send the DashScope API key to a caller-chosen endpoint through request or environment configuration. <br>
Mitigation: Use only official DashScope endpoints and avoid untrusted request JSON or DASHSCOPE_BASE_URL values. <br>
Risk: The helper script downloads the image URL returned by the API response. <br>
Mitigation: Run it in a reviewed environment with bounded output paths and a scoped, revocable API key. <br>


## Reference(s): <br>
- [Z-Image Turbo API Reference](references/api_reference.md) <br>
- [Official Z-Image API Reference](https://help.aliyun.com/zh/model-studio/z-image-api-reference) <br>
- [Official Z-Image API Reference (Alibaba Cloud)](https://www.alibabacloud.com/help/zh/model-studio/z-image-api-reference) <br>
- [Official Source Links](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, files] <br>
**Output Format:** [Markdown guidance with JSON request and response examples, shell commands, Python helper usage, and generated image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can download a generated image to the configured output path and optionally print normalized response JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
