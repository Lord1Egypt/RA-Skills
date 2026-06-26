## Description: <br>
Unified LLM Gateway - One API for 70+ AI models. Route to GPT, Claude, Gemini, Qwen, Deepseek, Grok and more with a single API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renning22](https://clawhub.ai/user/renning22) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to route chat, vision, model comparison, and fallback requests across multiple LLM providers through a single OpenAI-compatible AIsa gateway API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, conversation history, function schemas, image URLs, or image data may be sent to the AIsa gateway and possibly downstream model providers. <br>
Mitigation: Avoid submitting secrets, regulated data, internal URLs, or private images unless AIsa's privacy and retention terms meet the user's requirements. <br>
Risk: Using a shared or over-privileged API key can increase credential exposure and cost impact. <br>
Mitigation: Use a dedicated AISA_API_KEY, monitor usage and credits, and rotate the key if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/renning22/asia-llm-router-skills) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction) <br>
- [AIsa Model Pricing](https://marketplace.aisa.one/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with JSON examples, bash commands, and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the AISA_API_KEY environment variable and sends requests to the AIsa API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
