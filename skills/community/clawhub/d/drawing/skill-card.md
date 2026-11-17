## Description:

Generate children's drawings and coloring pages with modular prompts, style packs, and print-ready constraints across image models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn drawing, coloring-page, worksheet, or educational illustration requests into model-portable image prompts with age-appropriate style, composition, and print constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask the agent to remember drawing preferences or activation behavior, including outside the skill-local folder.

Mitigation: Confirm whether preference memory should be used, keep saved notes minimal, and honor paused or declined memory preferences.

Risk: Prompt text and optional reference images may be sent to the selected image provider, which can expose personal details or identifiable child photos.

Mitigation: Use generic descriptions where possible, avoid unnecessary personal details or identifiable child images, and use only trusted providers.

## Reference(s):

- [Drawing skill page](https://clawhub.ai/ivangdavila/skills/drawing)
- [Drawing homepage](https://clawic.com/skills/drawing)
- [OpenAI image generation guide](https://platform.openai.com/docs/guides/image-generation)
- [OpenAI cookbook image generation example](https://cookbook.openai.com/examples/generate_images_with_gpt_image)
- [Google Vertex AI image prompt guide](https://cloud.google.com/vertex-ai/generative-ai/docs/image/image-prompts-design)
- [OpenClaw models guide](https://docs.openclaw.ai/concepts/models)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with reusable image prompt templates, refinement guidance, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local preference memory under ~/drawing/ and provider-neutral image model workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
