## Description:

Generates six coordinated fashion marketing images from a clothing reference image or Pinterest pin, covering outfit, flat lay, detail, lifestyle, couple styling, and brand story visuals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z1o1u1s1](https://clawhub.ai/user/z1o1u1s1)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and fashion sellers use this skill to turn a clothing reference image or Pinterest pin into a coordinated set of social commerce visuals and publishing guidance for platforms such as Xiaohongshu and Pinterest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may copy the newest clipboard screenshot as a reference image without the user explicitly selecting that file, which can expose private or unintended visual content.

Mitigation: Ask the user to provide or approve the exact reference image path before using clipboard-derived screenshots or submitting any image to ImageGen.

Risk: Pinterest retrieval can return a generic fallback image instead of the intended pin image.

Mitigation: Validate the rendered page title, pin identifier, downloaded image hash, and image dimensions before using a Pinterest image as the generation reference.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/z1o1u1s1/skills/fashion-lookbook-generator)
- [Publisher profile](https://clawhub.ai/user/z1o1u1s1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Image files, Guidance]

**Output Format:** [Markdown guidance with ImageGen prompt text, command snippets for reference-image retrieval, and generated PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow targets six photorealistic outputs, typically in 3:4 or 2:3 aspect ratios, after previewing prompts and confirming generation cost.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
