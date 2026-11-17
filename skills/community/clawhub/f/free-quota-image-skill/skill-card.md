## Description:

Generate text-to-image outputs through a free-quota-first, multi-provider workflow with provider routing, token rotation, prompt optimization, fallback models, batch generation, and structured JSON results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chiayengu](https://clawhub.ai/user/chiayengu)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to generate images from prompts while routing across configured providers, rotating available tokens, and receiving stable JSON or image-file outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and API tokens may be sent to configured external image or text providers.

Mitigation: Use trusted HTTPS endpoints, low-privilege provider tokens, and avoid sensitive or proprietary prompt text.

Risk: The token status state file can contain full tokens in plaintext.

Mitigation: Review or remove token_status.json after use, prefer environment-based token injection, and keep local state out of shared deployments.

Risk: Prompt optimization can send prompt text to provider text models before image generation.

Mitigation: Disable prompt optimization for sensitive prompts or when provider-side prompt processing is not acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chiayengu/skills/free-quota-image-skill)
- [Project homepage](https://github.com/Amery2010/peinture)
- [Provider endpoints](references/provider-endpoints.md)
- [Model matrix](references/model-matrix.md)
- [Token rotation policy](references/token-rotation-policy.md)
- [Prompt optimization policy](references/prompt-optimization-policy.md)
- [OpenClaw integration](references/openclaw-integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, files, guidance]

**Output Format:** [Markdown guidance with CLI commands; runtime output is structured JSON, image URLs, and optional image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch mode returns a count and images array; failures return structured error_type, error, and fallback_chain fields.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
