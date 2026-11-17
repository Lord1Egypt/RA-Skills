## Description:

Unified LLM Gateway - One API for 70+ AI models. Route to GPT, Claude, Gemini, Qwen, Deepseek, Grok and more with a single API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renning22](https://clawhub.ai/user/renning22)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to route chat, streaming, vision, function-calling, and model-comparison requests through AISA's OpenAI-compatible gateway with a single AISA API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User prompts, system messages, image URLs or image data, and function schemas are routed through AISA's hosted API.

Mitigation: Avoid sending secrets, regulated data, private internal URLs, or confidential images unless your organization has approved AISA and its billing model.

Risk: The skill depends on an AISA_API_KEY and hosted model availability, pricing, and provider behavior.

Mitigation: Confirm provider approval, account credits, model availability, and cost controls before using it in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renning22/skills/asia-llm-router-skills)
- [OpenClaw](https://openclaw.ai)
- [AISA API reference](https://aisa.mintlify.app/api-reference/introduction)
- [AISA pricing and model list](https://marketplace.aisa.one/pricing)
- [AISA](https://aisa.one)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with curl examples, Python code, CLI commands, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and can send prompts, system messages, image URLs or data, and function schemas to AISA's hosted API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
