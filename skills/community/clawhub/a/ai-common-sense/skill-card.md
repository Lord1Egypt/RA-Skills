## Description:

Helps agents verify AI model names, versions, pricing, API IDs, deprecation status, and provider-specific API usage before answering or generating code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[futurizerush](https://clawhub.ai/user/futurizerush)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when comparing AI models, selecting current model IDs, checking API pricing, or generating provider API examples that need current names and endpoints. It is also useful when a prompt asks for the latest model, model comparison, model availability, or AI API pricing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled model, pricing, and deprecation references can become stale quickly.

Mitigation: Follow the skill's staleness rule and verify current model information with official provider sources when the last verified date is older than 30 days.

Risk: The included API examples are real external provider calls and reference provider API key environment variables.

Mitigation: Use restricted development keys, avoid sensitive prompts in examples, and review calls before execution.

Risk: The skill declares Bash, Read, WebSearch, and WebFetch permissions.

Mitigation: Install it only when an AI-model reference helper with web verification is needed, and limit or remove Bash permission if the runtime supports tighter tool scoping.

## Reference(s):

- [OpenAI model documentation](https://platform.openai.com/docs/models)
- [OpenAI pricing](https://openai.com/pricing)
- [Anthropic models documentation](https://docs.anthropic.com/en/docs/about-claude/models)
- [Anthropic pricing](https://docs.anthropic.com/en/docs/about-claude/pricing)
- [Google Gemini models documentation](https://ai.google.dev/gemini-api/docs/models)
- [Google Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Mistral model documentation](https://docs.mistral.ai/getting-started/models)
- [Mistral pricing](https://mistral.ai/pricing)
- [Cohere pricing](https://cohere.com/pricing)
- [Cohere changelog](https://docs.cohere.com/changelog)
- [Meta Llama 4 announcement](https://ai.meta.com/blog/llama-4-multimodal-intelligence/)
- [DeepSeek](https://deepseek.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with tables, provider references, API examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use web search and provider documentation when the included reference is older than 30 days.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
