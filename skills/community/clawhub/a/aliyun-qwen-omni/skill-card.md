## Description: <br>
Use when tasks require all-in-one multimodal understanding or generation with Alibaba Cloud Model Studio Qwen Omni models, including image-plus-audio interaction, voice assistants, and realtime multimodal agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to prepare and standardize Qwen Omni multimodal requests for image, audio, and text assistant workflows, realtime multimodal agents, and spoken responses grounded in visual input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This release is a lightweight request-template helper rather than a full Alibaba Cloud integration. <br>
Mitigation: Before providing credentials or sensitive inputs to any later version that adds real API calls, review the endpoint, required credentials, and data handling. <br>
Risk: The generated request payload includes demo input values and provider-specific model names. <br>
Mitigation: Replace demo values with approved inputs and verify supported Qwen Omni model names against Alibaba Cloud documentation before production use. <br>


## Reference(s): <br>
- [Qwen Omni documentation](https://help.aliyun.com/zh/model-studio/qwen-omni) <br>
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>
- [Sources](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, and JSON request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script writes a minimal Qwen Omni request JSON file and prints its output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
