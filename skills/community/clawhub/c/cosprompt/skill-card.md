## Description:

Cosprompt generates structured AI image prompts from a character or theme, using a 17-dimension framework for JSON, Markdown, and plain text outputs for tools such as Midjourney and Stable Diffusion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to turn character, cosplay, product, or scene ideas into structured prompts for image-generation tools. It is intended to help organize visual subject, style, composition, lighting, lens, typography, negative prompt, and aspect-ratio details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flagged under-18 age presets in a cosplay or glamour prompt workflow without clear safety boundaries.

Mitigation: Review or remove under-18 presets before deployment, or require that minors are depicted only in age-appropriate, non-sexual contexts without suggestive clothing, pose, body emphasis, or mood tags.

Risk: The artifact declares broad Write and Edit tool permissions for a prompt-generation workflow.

Mitigation: Remove file-modification permissions unless the deployment specifically requires the skill to modify local files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fslong520/skills/cosprompt)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [JSON, Markdown, and plain text prompt content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a 17-dimension image-prompt structure covering subject, age, model, face, pose, hair, costume, style, mood, environment, lighting, composition, lens, quality tags, typography, negative prompt, and aspect ratio.]

## Skill Version(s):

2.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
