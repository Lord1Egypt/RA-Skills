## Description:

Generates English prompts for Google Banana (Imagen series) text-to-image workflows, including Chinese explanations, negative prompts, and parameter suggestions for character, scene, storyboard, and concept art images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elevenzhou](https://clawhub.ai/user/elevenzhou)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, designers, and prompt writers use this skill to turn image-generation requests into structured Google Banana/Imagen prompts with reviewable Chinese explanations, negative prompts, and suggested image parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic image-prompt requests may be routed into a Banana/Imagen-specific prompt format that does not match the user's intended model.

Mitigation: Confirm the target image model when requests are ambiguous before applying Banana-specific structure or parameter suggestions.

Risk: The skill returns English prompts with Chinese explanations, which may not match every user's review workflow.

Mitigation: Ask users whether they want Chinese explanations preserved or adapted when language expectations are unclear.

## Reference(s):

- [Banana prompt template and examples](artifact/references/banana-prompt-template.md)
- [ClawHub release page](https://clawhub.ai/elevenzhou/skills/eleven-banana-prompt-generator)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown containing an English prompt, Chinese explanation, negative prompt, and parameter suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No tool execution or file output is evident; the agent returns prompt-writing guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
