## Description: <br>
Use when code generation, repository understanding, or coding-agent tasks need Alibaba Cloud Model Studio Qwen Coder models (`qwen3-coder-next`, `qwen3-coder-plus` and related coder variants). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent operators use this skill to prepare and document coding requests for Alibaba Cloud Model Studio Qwen Coder models, including repository context, model selection, target language, and reproducible output paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an external AI provider for coding tasks, so prompts or repository snippets may leave the local environment. <br>
Mitigation: Send only files needed for the task and avoid including secrets or unrelated proprietary code in prompts. <br>
Risk: API keys can be exposed through repositories, logs, or shared shell history. <br>
Mitigation: Use a dedicated DASHSCOPE_API_KEY or Alibaba Cloud credentials file and keep credentials out of source control and logs. <br>
Risk: Saved prompts and normalized request payloads may contain sensitive code or project context. <br>
Mitigation: Periodically review and clean output/aliyun-qwen-coder/ when request payloads may contain sensitive information. <br>


## Reference(s): <br>
- [Aliyun Qwen-Coder capabilities](https://help.aliyun.com/zh/model-studio/qwen-coder) <br>
- [Aliyun Model Studio model updates](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>
- [Aliyun Model Studio model list](https://help.aliyun.com/zh/model-studio/models) <br>
- [Aliyun Model Studio Cline integration](https://help.aliyun.com/zh/model-studio/cline) <br>
- [ClawHub release page](https://clawhub.ai/cinience/aliyun-qwen-coder) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and normalized JSON request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes request payloads under output/aliyun-qwen-coder/requests/ by default and records model, endpoint mode, language, framework, and repository context for reproducibility.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
