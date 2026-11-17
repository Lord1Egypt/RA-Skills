## Description:

Generates photorealistic images and Instagram-ready image-plus-caption content using Gemini image generation models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vitja1988](https://clawhub.ai/user/vitja1988)

### License/Terms of Use:


## Use Case:

Developers and content creators use this skill to generate standalone visual assets or Instagram-ready image and caption files from a prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports under-scoped instructions for separate Instagram posting automation.

Mitigation: Review the external posting workflow separately and do not run ig-automation smart_poster_v4.py commands unless automated account activity has been approved.

Risk: Prompts and API credential handling can expose sensitive data.

Mitigation: Use GEMINI_API_KEY rather than command-line API keys, avoid sensitive personal prompts, and install dependencies in an isolated environment.

## Reference(s):

- [Gemini API Reference](references/gemini_api.md)
- [Google AI Studio API Key](https://aistudio.google.com/app/apikey)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Gemini API Pricing](https://ai.google.dev/pricing)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration]

**Output Format:** [PNG, JPEG, or WebP image files and plain-text captions with Markdown command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses GEMINI_API_KEY and writes timestamped image files; Instagram post mode also writes a .txt caption next to the image.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
