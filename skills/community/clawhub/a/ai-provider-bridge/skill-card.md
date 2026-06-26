## Description: <br>
One interface to call 6 AI providers. Swap models with a config change, not a code rewrite. Zero external dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to call Anthropic, OpenAI, Google, xAI, Mistral, or local Ollama models through one JavaScript interface and switch providers by changing model configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, conversation history, and system prompts may be sent to external cloud AI providers when non-Ollama models are configured. <br>
Mitigation: Use Ollama for local-only processing, and send data to Anthropic, OpenAI, Google, xAI, or Mistral only when those providers are approved for the data and use case. <br>
Risk: Secrets, regulated data, or proprietary content could be exposed if included in prompts or provider configuration. <br>
Mitigation: Do not send sensitive content to cloud providers unless approved, and supply provider credentials through controlled environment variables or a secrets manager. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/ai-provider-bridge) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, API Calls, Configuration] <br>
**Output Format:** [JavaScript module responses and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses provider-specific API keys for cloud providers; Ollama can run locally without an API key.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
