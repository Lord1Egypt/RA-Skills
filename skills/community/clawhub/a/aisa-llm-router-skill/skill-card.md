## Description: <br>
Unified LLM Gateway - One API for 70+ AI models. Route to GPT, Claude, Gemini, Qwen, Deepseek, Grok and more with a single API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bowen-dotcom](https://clawhub.ai/user/bowen-dotcom) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to call multiple hosted LLM providers through AISA's OpenAI-compatible gateway, including chat, streaming, vision, model comparison, and fallback routing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, system messages, image URLs, and image data are sent to AISA and routed model providers. <br>
Mitigation: Use the skill only with providers you trust, avoid regulated or sensitive data unless approved, and review provider handling terms before production use. <br>
Risk: The AISA API key can be exposed through shell history, logs, screenshots, or shared scripts. <br>
Mitigation: Use a dedicated API key, store it in the environment or a secret manager, monitor usage and billing, and rotate it if exposure is suspected. <br>
Risk: Routed model availability, pricing, output quality, and downstream provider behavior can vary. <br>
Mitigation: Check current model availability and pricing, set token limits, monitor usage costs, and implement fallback handling for production workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bowen-dotcom/aisa-llm-router-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/bowen-dotcom) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [AISA API Reference](https://aisa.mintlify.app/api-reference/introduction) <br>
- [AISA Marketplace Pricing](https://marketplace.aisa.one/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with bash, Python, HTTP request examples, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and network access to the AISA API; routed prompts, system messages, image URLs, and image data are transmitted to AISA and downstream model providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
