## Description: <br>
Generates and prepares text generation, reasoning, chat, tool-calling, and long-context workflows for Alibaba Cloud Model Studio Qwen text models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to select Alibaba Cloud Model Studio Qwen text models, prepare normalized generation requests, and document reproducible request examples for text, chat, reasoning, tool-calling, and long-context workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and request parameters are sent to Alibaba Cloud Model Studio when API examples are executed. <br>
Mitigation: Use this skill only for approved Alibaba Cloud workflows and avoid sending secrets or regulated data unless that provider is approved for the data. <br>
Risk: API credentials are required through DASHSCOPE_API_KEY or Alibaba Cloud credentials. <br>
Mitigation: Use a scoped API key and keep credentials in the environment or approved credential storage rather than request files or prompts. <br>
Risk: The helper writes request payload files under output/aliyun-qwen-generation/. <br>
Mitigation: Review generated files before sharing or committing them, especially when prompts may contain private content. <br>


## Reference(s): <br>
- [Artifact reference sources](references/sources.md) <br>
- [Alibaba Cloud Model Studio model releases](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>
- [Alibaba Cloud Model Studio text generation models](https://help.aliyun.com/zh/model-studio/models) <br>
- [Alibaba Cloud Model Studio text generation overview](https://help.aliyun.com/zh/model-studio/text-generation) <br>
- [Alibaba Cloud Model Studio OpenAI-compatible API](https://help.aliyun.com/zh/model-studio/openai-compatible) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request payload files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes normalized request JSON under output/aliyun-qwen-generation/requests/ when the helper script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
