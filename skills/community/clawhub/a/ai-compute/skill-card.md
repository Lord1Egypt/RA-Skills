## Description:

27-endpoint AI compute skill — LLM inference, image generation, video generation, text-to-speech, speech-to-text, embeddings, GPU inference, Bittensor decentralized AI, on-chain AI analytics, and prepaid compute futures via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to request AI inference, media generation, embeddings, and on-chain analysis through x402 endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid calls and prepaid credit operations can spend real USDC.

Mitigation: Before each paid call, show the endpoint, estimated cost, and input data, then wait for explicit approval; enforce a per-session spending cap and require two confirmations for deposits and refunds.

Risk: Prompts, media, audio URLs, and wallet addresses are sent to the gateway and external AI providers.

Mitigation: Get approval before transmitting content and exclude secrets, private keys, personal data, and confidential material.

Risk: The helper script referenced by the skill is missing from the supplied package, so its implementation was not inspected.

Mitigation: Review the helper before supplying an API key or funds; use only documented endpoints and test on devnet where available.

## Reference(s):

- [AI Compute on ClawHub](https://clawhub.ai/plagtech/skills/ai-compute)
- [Spraay gateway](https://gateway.spraay.app)

## Skill Output:

**Output Type(s):** [API responses, Text, JSON, Images, Audio, Video, Embeddings]

**Output Format:** [Structured API responses or generated media, depending on the selected endpoint]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Endpoint-dependent; may include text, media, embedding data, or job status.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
