## Description: <br>
Helps agents edit existing images with Alibaba Cloud Model Studio Qwen Image Edit models, including inpainting, replacement, style transfer, local edits, subject consistency, and request/response mapping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and image workflow operators use this skill to prepare, execute, and document Alibaba Cloud Qwen Image Edit requests for instruction-based edits to existing images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images, prompts, and edit payloads may contain sensitive content that is sent to Alibaba Cloud Model Studio. <br>
Mitigation: Use approved input images and prompts, prefer a dedicated DashScope key, and avoid sending sensitive content unless the user has confirmed the cloud processing path. <br>
Risk: Saved request/response payloads and result URLs can expose edit details if retained or committed. <br>
Mitigation: Keep output directories out of source control and redact or delete saved payloads after sensitive edits. <br>


## Reference(s): <br>
- [Alibaba Cloud Qwen Image Edit Guide](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide) <br>
- [Alibaba Cloud Model Studio Newly Released Models](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>
- [ClawHub Skill Page](https://clawhub.ai/cinience/aliyun-qwen-image-edit) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code, JSON files] <br>
**Output Format:** [Markdown guidance with bash examples and generated JSON request files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes normalized request payloads and validation results under output/aliyun-qwen-image-edit/ unless OUTPUT_DIR is set.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
