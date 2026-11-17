## Description:

Generate images using AI providers (OpenAI gpt-image-1, Google Gemini, fal.ai) when the user asks to create, generate, or make an image, picture, illustration, photo, artwork, or visual content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lumenclaw-cloud](https://clawhub.ai/user/lumenclaw-cloud)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill to generate and edit images through OpenAI, Gemini, or fal.ai using their own provider API keys. It is suited for creating visual content, editing existing images, and getting prompt-writing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider API calls can spend user-supplied API key budget and send prompts or images to the selected provider.

Mitigation: Use only API keys approved for this workflow, monitor provider usage, and avoid private images or sensitive prompts unless the provider and account controls are trusted.

Risk: fal.ai image editing disables a provider safety checker by default.

Mitigation: Review fal.ai outputs before use and enable or enforce appropriate provider safety controls before sensitive or production workflows.

Risk: The skill downloads provider-returned image URLs without URL validation.

Mitigation: Use trusted providers and harden URL validation or network egress controls before running in sensitive or network-restricted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lumenclaw-cloud/skills/filtrix-image-gen-v2)
- [Prompt Writing Guide](references/prompts.md)
- [OpenAI Image Generation](references/openai.md)
- [Gemini Image Generation](references/gemini.md)
- [fal.ai Image Generation](references/fal.md)
- [Filtrix AI Prompt Library](https://www.filtrix.ai/prompts)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG image files saved to disk with terminal status output and Markdown guidance when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied OpenAI, Gemini, or fal.ai API keys and may write generated or edited images to a requested output path or to /tmp by default.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
