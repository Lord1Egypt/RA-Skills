## Description:

Generate and edit images using OpenAI gpt-image-1, Google Gemini, and fal.ai models with user-supplied API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lumenclaw-cloud](https://clawhub.ai/user/lumenclaw-cloud)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill to generate new images from prompts or edit existing images through supported provider APIs. It is suited for agent-assisted visual content creation where the user controls provider choice, model, size, and output path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected images, and masks may be sent to external providers including OpenAI, Google, and fal.ai.

Mitigation: Use the skill only with content that is acceptable to share with the selected provider under that provider's terms.

Risk: The fal.ai edit path disables a provider-side safety checker without a user-facing option or disclosure.

Mitigation: Review prompts and source images before using fal.ai edits, and prefer providers with active safety filtering for sensitive or policy-critical workflows.

## Reference(s):

- [OpenAI Image Generation](references/openai.md)
- [Gemini Image Generation](references/gemini.md)
- [fal.ai Image Generation](references/fal.md)
- [Prompt Writing Guide](references/prompts.md)
- [Filtrix AI Prompt Library](https://www.filtrix.ai/prompts)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash commands and generated PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied provider API keys; scripts print the local image path and byte size on success.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
