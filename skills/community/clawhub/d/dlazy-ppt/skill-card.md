## Description:

Generate visually unified image-based PPT/PPTX decks from articles, reports, papers, notes, or outlines, using dLazy for every slide image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and presenters use this skill to turn articles, reports, papers, notes, or outlines into visually unified slide decks and a PPTX. Each slide is a full-page image, so its text and visual elements are not separately editable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Slide content and source images are sent to dLazy for slide image generation.

Mitigation: Review source material and images for sensitive information before generating a deck.

Risk: Image generation uses an API key and can be configured with a custom API destination.

Mitigation: Protect DLAZY_API_KEY and use only a trusted HTTPS DLAZY_BASE_URL.

## Reference(s):

- [dLazy AI PPT Slides project](https://github.com/dlazy-ai/ai-ppt-slides)
- [dLazy API key setup](https://dlazy.com/dashboard/organization/api-key)
- [Image generation and configuration guide](https://github.com/dlazy-ai/ai-ppt-slides/blob/main/docs/image-generation-cli.md)
- [Image model configuration guide](https://github.com/dlazy-ai/ai-ppt-slides/blob/main/docs/image-model-configuration.md)

## Skill Output:

**Output Type(s):** [Files, Images, Markdown, JSON]

**Output Format:** [PPTX presentation, PNG slide images, Markdown outline and speaker notes, and JSON project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Slides are full-page images; individual slide text and visual elements are not separately editable.]

## Skill Version(s):

1.0.32 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
