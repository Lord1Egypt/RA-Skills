## Description: <br>
The Baidu AI Studio LLM API Assistant helps developers connect to Baidu AI Studio large-model API services, use OpenAI-compatible Python SDK workflows, and work with models such as ERNIE and DeepSeek. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lemonteeeeaa](https://clawhub.ai/user/lemonteeeeaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to configure Baidu AI Studio API access, choose supported models, and generate OpenAI SDK-compatible examples for chat completions, streaming, function calling, structured output, multimodal input, image generation, and embeddings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an API token for Baidu AI Studio. <br>
Mitigation: Keep AI_STUDIO_API_KEY private, avoid committing .env files, and verify the publisher and Baidu documentation before entering a token. <br>
Risk: Prompts, images, video URLs, embeddings, and other request data may be sent to Baidu AI Studio API endpoints. <br>
Mitigation: Do not send sensitive data unless Baidu AI Studio processing is acceptable for the intended use case. <br>


## Reference(s): <br>
- [Baidu AI Studio API documentation](https://ai.baidu.com/ai-doc/AISTUDIO/rm344erns) <br>
- [Baidu AI Studio access token page](https://aistudio.baidu.com/account/accessToken) <br>
- [OpenClaw Skill installation tutorial](https://dcn8t60z51f3.feishu.cn/wiki/DiiFwvRMoiQe1MkYqLacwsuWnZb) <br>
- [API parameter reference](references/api_params.md) <br>
- [Model reference](references/models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include configuration steps that use AI_STUDIO_API_KEY and examples that send requests to Baidu AI Studio API endpoints.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
