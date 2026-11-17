## Description:

The Baidu AI Studio LLM API Assistant helps developers connect agents to Baidu AI Studio large-model services, including ERNIE and DeepSeek models, through an OpenAI-compatible Python SDK workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lemonteeeeaa](https://clawhub.ai/user/lemonteeeeaa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure credentials, choose models, and generate OpenAI-compatible Python calls for Baidu AI Studio chat, search-augmented, function-calling, multimodal, image-generation, and embedding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance can expose the AI_STUDIO_API_KEY token if users print it or store it carelessly.

Mitigation: Use a virtual environment and a secret manager or protected environment variable; do not run commands that print the token, and keep local .env files out of source control.

Risk: The skill installs the openai dependency without a pinned version.

Mitigation: Pin the openai package version before installation and review dependency changes during upgrades.

Risk: Prompts, files, image URLs, search queries, and embeddings input may be sent to Baidu AI Studio services.

Mitigation: Review Baidu AI Studio policies and avoid sending sensitive, regulated, or proprietary data unless approved for that provider.

## Reference(s):

- [Model Reference](references/models.md)
- [API Parameter Reference](references/api_params.md)
- [Baidu AI Studio API Documentation](https://ai.baidu.com/ai-doc/AISTUDIO/rm344erns)
- [Baidu AI Studio Access Token](https://aistudio.baidu.com/account/accessToken)
- [OpenClaw Installation Tutorial](https://dcn8t60z51f3.feishu.cn/wiki/DiiFwvRMoiQe1MkYqLacwsuWnZb)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include credential setup guidance, model recommendations, and OpenAI-compatible API call examples for Baidu AI Studio services.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
