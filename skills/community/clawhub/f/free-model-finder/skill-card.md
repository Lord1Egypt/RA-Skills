## Description:

帮助用户发现、比较并配置 OpenRouter、HuggingFace、Groq、Google AI Studio 和 Ollama 等平台的免费或低价 AI 模型，并支持成本优化和限流后的备用模型切换。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sucriss](https://clawhub.ai/user/sucriss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to find free or low-cost AI models, compare platform tradeoffs, and configure primary and fallback models to reduce inference cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The auto and switch workflows can rewrite the local OpenClaw model configuration.

Mitigation: Review the exact changes before use and back up ~/.openclaw/openclaw.json first.

Risk: Provider API keys are required for several platforms and may be stored locally when configured through OpenClaw.

Mitigation: Configure only keys you own and treat local OpenClaw environment settings as sensitive.

Risk: The publish guide includes an unpinned npx install example.

Mitigation: Avoid npx commands that install @latest unless the current package source is trusted.

Risk: Model availability, pricing, and rate limits can change after release.

Mitigation: Confirm provider terms and quotas before applying a recommended model configuration.

## Reference(s):

- [Platform details](references/platforms.md)
- [OpenRouter API keys](https://openrouter.ai/keys)
- [Groq API keys](https://console.groq.com/keys)
- [Google AI Studio API keys](https://aistudio.google.com/app/apikey)
- [Hugging Face tokens](https://huggingface.co/settings/tokens)
- [Ollama](https://ollama.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown or terminal text with inline shell commands and JSON configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read provider API key environment variables and may update the local OpenClaw model configuration.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact files list 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
