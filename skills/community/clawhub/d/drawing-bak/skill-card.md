## Description:

Generate children's drawings and coloring pages with modular prompts, style packs, and print-ready constraints across image models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[12357851](https://clawhub.ai/user/12357851)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn drawing, coloring-page, worksheet, and educational-illustration requests into kid-safe, model-portable image prompts. It helps choose an output mode, age-appropriate detail level, style pack, print constraints, and refinement steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may record drawing preferences, age bands, style choices, and activation behavior in memory, including shared memory outside its declared local folder.

Mitigation: Review memory behavior before installation and keep drawing-related notes limited to ~/drawing/ unless shared memory is explicitly acceptable.

Risk: Prompt text and optional reference images may be sent to the selected image provider.

Mitigation: Use only trusted providers and avoid sending unnecessary personal details or identifiable child photos when a generic description is sufficient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/12357851/skills/drawing-bak)
- [OpenAI image generation guide](https://platform.openai.com/docs/guides/image-generation)
- [OpenAI Cookbook image generation example](https://cookbook.openai.com/examples/generate_images_with_gpt_image)
- [Google Vertex AI image prompt guide](https://cloud.google.com/vertex-ai/generative-ai/docs/image/image-prompts-design)
- [OpenClaw models documentation](https://docs.openclaw.ai/concepts/models)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with reusable prompt templates and occasional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain local drawing preferences and reusable prompt notes under ~/drawing/.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
