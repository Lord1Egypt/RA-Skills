## Description: <br>
Edit images with Alibaba Cloud Model Studio Qwen Image Edit models (qwen-image-edit, qwen-image-edit-plus, qwen-image-edit-max and snapshots). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and image-workflow builders use this skill to prepare and document Alibaba Cloud Qwen Image Edit requests for inpainting, replacement, style transfer, local edits, and subject-consistent modifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alibaba Cloud DashScope credentials may be exposed through source control, logs, or shared environments. <br>
Mitigation: Use a dedicated API key where possible, provide it through DASHSCOPE_API_KEY or the Alibaba Cloud credentials file, and keep credentials out of source control and logs. <br>
Risk: Local output files may contain private prompts, image URLs, model parameters, or generated result references. <br>
Mitigation: Review output files before sharing, store generated assets in appropriate object storage, and persist only URLs or sanitized metadata when possible. <br>
Risk: Unpinned DashScope SDK installs can change behavior across environments. <br>
Mitigation: Pin the dashscope SDK version for reproducible installs when deploying the skill in a managed workflow. <br>


## Reference(s): <br>
- [Artifact reference sources](references/sources.md) <br>
- [Alibaba Cloud Model Studio Qwen Image Edit guide](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide) <br>
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON request files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save edit request payloads, result URLs, model parameters, and image output references under output/alicloud-ai-image-qwen-image-edit/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
