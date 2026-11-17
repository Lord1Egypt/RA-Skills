## Description:

Unified LLM Gateway - One API for 70+ AI models. Route to GPT, Claude, Gemini, Qwen, Deepseek, Grok and more with a single API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-dotcom](https://clawhub.ai/user/bowen-dotcom)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to call AIsa's OpenAI-compatible LLM gateway for chat, streaming responses, vision analysis, function calling, model comparison, and model listing through one API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, message histories, image URLs or base64 images, and tool/function schemas are sent to AIsa and may be routed to downstream model providers.

Mitigation: Use the skill only for data approved for that sharing path; avoid secrets, regulated data, internal signed URLs, and confidential documents unless approval is documented.

Risk: The skill requires an AISA_API_KEY for API calls.

Mitigation: Provide the key through the environment and do not paste it into prompts, committed files, or shared command transcripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bowen-dotcom/skills/aisa-llm-router-skill)
- [OpenClaw](https://openclaw.ai)
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction)
- [AIsa Pricing](https://marketplace.aisa.one/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python code, and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; supports chat, streaming, vision, model listing, and model comparison workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
