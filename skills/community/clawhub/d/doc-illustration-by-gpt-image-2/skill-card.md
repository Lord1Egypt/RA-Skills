## Description:

Generates polished technical-document illustrations, infographics, and repo architecture visuals with OpenAI GPT Image 2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eriklee1895](https://clawhub.ai/user/eriklee1895)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and technical writers use this skill to turn briefs, design notes, Markdown specs, and codebase explanations into document-ready illustrations. It supports text-only generation, reference-image style guidance, and dry-run prompt review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, briefs, and reference images may be sent to the selected OpenAI-compatible image provider.

Mitigation: Use the skill only with documents and images that are approved for the selected provider, and prefer the official OpenAI endpoint for sensitive work.

Risk: A configurable OPENAI_BASE_URL can route requests to an unintended provider.

Mitigation: Verify OPENAI_BASE_URL before live generation and clear it when the official endpoint should be used.

Risk: Generated JSON sidecars may contain private prompts, briefs, or image paths.

Mitigation: Keep sidecar metadata out of shared repositories when it contains private or sensitive content.

## Reference(s):

- [Skill package](https://clawhub.ai/eriklee1895/skills/doc-illustration-by-gpt-image-2)
- [OpenAI Image Workflow](references/openai-image-workflow.md)
- [OpenAI Official Links](references/openai-official-links.md)
- [Prompt Patterns](references/prompt-patterns.md)
- [Style Profiles](references/style-profiles.md)
- [GPT Image 2 model page](https://developers.openai.com/api/docs/models/gpt-image-2)
- [OpenAI image generation guide](https://developers.openai.com/api/docs/guides/image-generation)
- [OpenAI Images API Python reference](https://developers.openai.com/api/reference/python/resources/images)

## Skill Output:

**Output Type(s):** [Files, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [PNG image files with JSON sidecar metadata and a Markdown image snippet; dry-run emits JSON prompt metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text-only and reference-plus-text modes, predefined style profiles, and document-oriented size presets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
