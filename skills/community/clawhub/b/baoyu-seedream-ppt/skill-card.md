## Description:

Generates image-based PPT decks from user content by combining Baoyu infographic layouts and styles with Doubao Seedream image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cindypapa](https://clawhub.ai/user/cindypapa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn structured source material into presentation-ready image slides and a PPTX deck. It supports an interactive review flow for layout, style, aspect ratio, and prompt confirmation before image generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Slide content and generated prompts are sent to Volcengine Seedream for image generation.

Mitigation: Use non-sensitive material and confirm users are comfortable with external image-generation processing before running generation.

Risk: Unsafe path handling may expose local Markdown files or write outputs outside the intended folder.

Mitigation: Avoid untrusted config files and custom layout, style, project, or output path values unless allowlists and output-directory containment are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cindypapa/skills/baoyu-seedream-ppt)
- [Project homepage](https://github.com/JimLiu/baoyu-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance, saved prompt Markdown files, generated PNG images, and a PPTX deck]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Volcengine API key and produces one generated image per slide before assembling the final deck.]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
